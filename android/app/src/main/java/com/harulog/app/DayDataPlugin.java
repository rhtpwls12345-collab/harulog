package com.harulog.app;

import android.Manifest;
import android.content.ContentResolver;
import android.content.ContentUris;
import android.content.Intent;
import android.database.Cursor;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Matrix;
import android.media.ExifInterface;
import android.net.Uri;
import android.os.Build;
import android.provider.CalendarContract;
import android.provider.MediaStore;
import android.provider.Settings;
import android.util.Base64;
import android.util.Size;

import androidx.core.content.ContextCompat;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.PermissionState;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;
import com.getcapacitor.annotation.Permission;
import com.getcapacitor.annotation.PermissionCallback;

import java.io.ByteArrayOutputStream;
import java.io.InputStream;

/**
 * 하루로그 DayData: 하루 초안을 만들기 위한 기기 데이터 (모두 읽기 전용, 기기 밖으로 보내지 않음)
 *  - 캘린더: CalendarContract.Instances (제목·시작·끝·장소·캘린더 이름)
 *  - 사진: MediaStore 사진의 찍은 시각 목록 + 고른 사진의 축소 JPEG
 *  - 이동 수단: 구글 활동 인식 Transition API 기록 (TransitionReceiver 가 저장)
 */
@CapacitorPlugin(
    name = "DayData",
    permissions = {
        @Permission(alias = "calendar", strings = { Manifest.permission.READ_CALENDAR }),
        @Permission(alias = "photos", strings = { "android.permission.READ_MEDIA_IMAGES" }),
        @Permission(alias = "photosPartial", strings = { "android.permission.READ_MEDIA_VISUAL_USER_SELECTED" }),
        @Permission(alias = "photosLegacy", strings = { Manifest.permission.READ_EXTERNAL_STORAGE }),
        @Permission(alias = "activity", strings = { "android.permission.ACTIVITY_RECOGNITION" })
    }
)
public class DayDataPlugin extends Plugin {

    private boolean granted(String perm) {
        return ContextCompat.checkSelfPermission(getContext(), perm) == android.content.pm.PackageManager.PERMISSION_GRANTED;
    }

    private String stateOf(String alias) {
        PermissionState s = getPermissionState(alias);
        return s == null ? "prompt" : s.toString(); // granted | denied | prompt | prompt-with-rationale
    }

    private String photoState() {
        if (Build.VERSION.SDK_INT >= 33) {
            if (granted("android.permission.READ_MEDIA_IMAGES")) return "granted";
            if (Build.VERSION.SDK_INT >= 34 && granted("android.permission.READ_MEDIA_VISUAL_USER_SELECTED")) return "limited";
            return stateOf("photos");
        }
        return granted(Manifest.permission.READ_EXTERNAL_STORAGE) ? "granted" : stateOf("photosLegacy");
    }

    private String activityState() {
        if (!TransitionTracker.playServicesAvailable(getContext())) return "unavailable";
        if (Build.VERSION.SDK_INT < 29) return "granted"; // Android 9 이하는 설치 시 허용
        return granted("android.permission.ACTIVITY_RECOGNITION") ? "granted" : stateOf("activity");
    }

    @PluginMethod
    public void checkAccess(PluginCall call) {
        JSObject ret = new JSObject();
        ret.put("calendar", granted(Manifest.permission.READ_CALENDAR) ? "granted" : stateOf("calendar"));
        ret.put("photos", photoState());
        ret.put("activity", activityState());
        ret.put("tracking", TransitionTracker.isEnabled(getContext()) && "granted".equals(activityState()));
        call.resolve(ret);
    }

    /** { kind: 'calendar' | 'photos' | 'activity' } */
    @PluginMethod
    public void requestAccess(PluginCall call) {
        String kind = call.getString("kind", "");
        switch (kind) {
            case "calendar":
                requestPermissionForAlias("calendar", call, "accessCallback");
                break;
            case "photos":
                if (Build.VERSION.SDK_INT >= 34) requestPermissionForAliases(new String[] { "photos", "photosPartial" }, call, "accessCallback");
                else if (Build.VERSION.SDK_INT >= 33) requestPermissionForAlias("photos", call, "accessCallback");
                else requestPermissionForAlias("photosLegacy", call, "accessCallback");
                break;
            case "activity":
                if (Build.VERSION.SDK_INT < 29) { checkAccess(call); return; }
                requestPermissionForAlias("activity", call, "accessCallback");
                break;
            default:
                call.reject("알 수 없는 권한 종류: " + kind);
        }
    }

    @PermissionCallback
    private void accessCallback(PluginCall call) {
        checkAccess(call);
    }

    @PluginMethod
    public void openAppSettings(PluginCall call) {
        Intent i = new Intent(Settings.ACTION_APPLICATION_DETAILS_SETTINGS, Uri.parse("package:" + getContext().getPackageName()));
        i.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        getContext().startActivity(i);
        call.resolve();
    }

    /* ---------------- 캘린더 ---------------- */

    /** { start, end } (epoch ms) → { events: [{ id, title, begin, end, allDay, location, calendar }] } */
    @PluginMethod
    public void getEvents(PluginCall call) {
        if (!granted(Manifest.permission.READ_CALENDAR)) { call.reject("캘린더 권한이 없어요", "NO_PERMISSION"); return; }
        long start = call.getLong("start", 0L), end = call.getLong("end", 0L);
        if (end <= start) { call.reject("기간이 올바르지 않아요"); return; }
        Uri.Builder b = CalendarContract.Instances.CONTENT_URI.buildUpon();
        ContentUris.appendId(b, start);
        ContentUris.appendId(b, end);
        String[] proj = {
            CalendarContract.Instances.EVENT_ID, CalendarContract.Instances.TITLE, CalendarContract.Instances.BEGIN,
            CalendarContract.Instances.END, CalendarContract.Instances.ALL_DAY, CalendarContract.Instances.EVENT_LOCATION,
            CalendarContract.Instances.CALENDAR_DISPLAY_NAME, CalendarContract.Instances.SELF_ATTENDEE_STATUS
        };
        JSArray out = new JSArray();
        try (Cursor c = getContext().getContentResolver().query(b.build(), proj,
                CalendarContract.Instances.VISIBLE + "=1", null, CalendarContract.Instances.BEGIN + " ASC")) {
            while (c != null && c.moveToNext()) {
                if (c.getInt(7) == CalendarContract.Attendees.ATTENDEE_STATUS_DECLINED) continue;
                JSObject o = new JSObject();
                o.put("id", c.getLong(0));
                o.put("title", c.getString(1));
                o.put("begin", c.getLong(2));
                o.put("end", c.getLong(3));
                o.put("allDay", c.getInt(4) == 1);
                o.put("location", c.getString(5));
                o.put("calendar", c.getString(6));
                out.put(o);
            }
        } catch (Exception e) {
            call.reject("캘린더를 읽지 못했어요: " + e.getMessage());
            return;
        }
        JSObject ret = new JSObject();
        ret.put("events", out);
        call.resolve(ret);
    }

    /* ---------------- 사진 ---------------- */

    /** { start, end } → { photos: [{ id, time, width, height, screenshot }] } (파일 이름·위치 정보는 넘기지 않음) */
    @PluginMethod
    public void getPhotos(PluginCall call) {
        String st = photoState();
        if (!"granted".equals(st) && !"limited".equals(st)) { call.reject("사진 권한이 없어요", "NO_PERMISSION"); return; }
        long start = call.getLong("start", 0L), end = call.getLong("end", 0L);
        Uri uri = MediaStore.Images.Media.EXTERNAL_CONTENT_URI;
        String[] proj = {
            MediaStore.Images.Media._ID, MediaStore.Images.Media.DATE_TAKEN, MediaStore.Images.Media.DATE_ADDED,
            MediaStore.Images.Media.WIDTH, MediaStore.Images.Media.HEIGHT, MediaStore.Images.Media.BUCKET_DISPLAY_NAME
        };
        String sel = "(" + MediaStore.Images.Media.DATE_TAKEN + " >= ? AND " + MediaStore.Images.Media.DATE_TAKEN + " < ?) OR ("
            + MediaStore.Images.Media.DATE_TAKEN + " IS NULL AND " + MediaStore.Images.Media.DATE_ADDED + " >= ? AND " + MediaStore.Images.Media.DATE_ADDED + " < ?)";
        String[] args = { String.valueOf(start), String.valueOf(end), String.valueOf(start / 1000), String.valueOf(end / 1000) };
        JSArray out = new JSArray();
        try (Cursor c = getContext().getContentResolver().query(uri, proj, sel, args, MediaStore.Images.Media.DATE_TAKEN + " ASC")) {
            int n = 0;
            while (c != null && c.moveToNext() && n < 500) {
                long taken = c.isNull(1) ? c.getLong(2) * 1000L : c.getLong(1);
                String bucket = c.getString(5);
                String lb = bucket == null ? "" : bucket.toLowerCase();
                JSObject o = new JSObject();
                o.put("id", String.valueOf(c.getLong(0)));
                o.put("time", taken);
                o.put("width", c.getInt(3));
                o.put("height", c.getInt(4));
                o.put("screenshot", lb.contains("screenshot") || lb.contains("스크린샷") || lb.contains("screen"));
                out.put(o);
                n++;
            }
        } catch (Exception e) {
            call.reject("사진 목록을 읽지 못했어요: " + e.getMessage());
            return;
        }
        JSObject ret = new JSObject();
        ret.put("photos", out);
        call.resolve(ret);
    }

    /** { id, max } → { dataUrl } 긴 변이 max px 이하인 JPEG */
    @PluginMethod
    public void getPhoto(PluginCall call) {
        String id = call.getString("id");
        int max = Math.max(64, Math.min(2048, call.getInt("max", 1280)));
        if (id == null || !id.matches("\\d{1,19}")) { call.reject("사진 id가 올바르지 않아요"); return; }
        Uri uri = ContentUris.withAppendedId(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, Long.parseLong(id));
        ContentResolver cr = getContext().getContentResolver();
        try {
            Bitmap bmp;
            if (Build.VERSION.SDK_INT >= 29) {
                bmp = cr.loadThumbnail(uri, new Size(max, max), null); // 회전 정보 반영됨
            } else {
                BitmapFactory.Options o = new BitmapFactory.Options();
                o.inJustDecodeBounds = true;
                try (InputStream in = cr.openInputStream(uri)) { BitmapFactory.decodeStream(in, null, o); }
                int sample = 1;
                while (Math.max(o.outWidth, o.outHeight) / (sample * 2) >= max) sample *= 2;
                BitmapFactory.Options o2 = new BitmapFactory.Options();
                o2.inSampleSize = sample;
                try (InputStream in = cr.openInputStream(uri)) { bmp = BitmapFactory.decodeStream(in, null, o2); }
                int deg = 0;
                try (InputStream in = cr.openInputStream(uri)) {
                    int ori = new ExifInterface(in).getAttributeInt(ExifInterface.TAG_ORIENTATION, ExifInterface.ORIENTATION_NORMAL);
                    deg = ori == ExifInterface.ORIENTATION_ROTATE_90 ? 90 : ori == ExifInterface.ORIENTATION_ROTATE_180 ? 180 : ori == ExifInterface.ORIENTATION_ROTATE_270 ? 270 : 0;
                } catch (Exception ignored) {}
                if (bmp != null && deg != 0) {
                    Matrix m = new Matrix();
                    m.postRotate(deg);
                    bmp = Bitmap.createBitmap(bmp, 0, 0, bmp.getWidth(), bmp.getHeight(), m, true);
                }
            }
            if (bmp == null) { call.reject("사진을 열지 못했어요"); return; }
            float k = Math.min(1f, (float) max / Math.max(bmp.getWidth(), bmp.getHeight()));
            if (k < 1f) bmp = Bitmap.createScaledBitmap(bmp, Math.round(bmp.getWidth() * k), Math.round(bmp.getHeight() * k), true);
            ByteArrayOutputStream bos = new ByteArrayOutputStream();
            bmp.compress(Bitmap.CompressFormat.JPEG, 82, bos);
            JSObject ret = new JSObject();
            ret.put("dataUrl", "data:image/jpeg;base64," + Base64.encodeToString(bos.toByteArray(), Base64.NO_WRAP));
            call.resolve(ret);
        } catch (Exception e) {
            call.reject("사진을 열지 못했어요: " + e.getMessage());
        }
    }

    /* ---------------- 이동 수단 ---------------- */

    @PluginMethod
    public void startMoveTracking(PluginCall call) {
        if (!"granted".equals(activityState())) { call.reject("신체 활동 권한이 없어요", "NO_PERMISSION"); return; }
        TransitionTracker.start(getContext(), new TransitionTracker.Done() {
            @Override public void ok() { call.resolve(); }
            @Override public void fail(String msg) { call.reject(msg); }
        });
    }

    @PluginMethod
    public void stopMoveTracking(PluginCall call) {
        TransitionTracker.stop(getContext());
        call.resolve();
    }

    /** { start, end } → { transitions: [{ time, activity, kind }] } */
    @PluginMethod
    public void getTransitions(PluginCall call) {
        long start = call.getLong("start", 0L), end = call.getLong("end", System.currentTimeMillis());
        JSObject ret = new JSObject();
        ret.put("transitions", TransitionTracker.read(getContext(), start, end));
        call.resolve(ret);
    }
}
