package com.harulog.app;

import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.GoogleApiAvailability;
import com.google.android.gms.location.ActivityRecognition;
import com.google.android.gms.location.ActivityTransition;
import com.google.android.gms.location.ActivityTransitionRequest;
import com.google.android.gms.location.DetectedActivity;

import org.json.JSONArray;
import org.json.JSONObject;

import java.util.ArrayList;
import java.util.List;

/** 활동 인식 전환(걷기·달리기·자전거·차량·정지 시작/끝)을 등록하고, 받은 기록을 기기 안에 14일치 보관한다. */
public final class TransitionTracker {
    interface Done { void ok(); void fail(String msg); }

    private static final String PREFS = "harulog_moves";
    private static final String KEY_ON = "enabled";
    private static final String KEY_LOG = "log";
    private static final long KEEP_MS = 14L * 24 * 3600_000L;
    private static final int MAX_ENTRIES = 3000;

    private TransitionTracker() {}

    static boolean playServicesAvailable(Context ctx) {
        try {
            return GoogleApiAvailability.getInstance().isGooglePlayServicesAvailable(ctx) == ConnectionResult.SUCCESS;
        } catch (Throwable t) {
            return false;
        }
    }

    static boolean isEnabled(Context ctx) {
        return prefs(ctx).getBoolean(KEY_ON, false);
    }

    private static SharedPreferences prefs(Context ctx) {
        return ctx.getApplicationContext().getSharedPreferences(PREFS, Context.MODE_PRIVATE);
    }

    private static PendingIntent pendingIntent(Context ctx) {
        Intent i = new Intent(ctx.getApplicationContext(), TransitionReceiver.class);
        i.setAction("com.harulog.app.ACTIVITY_TRANSITION");
        int flags = PendingIntent.FLAG_UPDATE_CURRENT;
        if (Build.VERSION.SDK_INT >= 31) flags |= PendingIntent.FLAG_MUTABLE; // 활동 인식 결과를 담아 보내려면 mutable 이어야 함
        return PendingIntent.getBroadcast(ctx.getApplicationContext(), 7301, i, flags);
    }

    @SuppressWarnings("MissingPermission")
    static void start(Context ctx, Done done) {
        List<ActivityTransition> list = new ArrayList<>();
        int[] types = { DetectedActivity.WALKING, DetectedActivity.RUNNING, DetectedActivity.ON_BICYCLE, DetectedActivity.IN_VEHICLE, DetectedActivity.STILL };
        for (int t : types) {
            list.add(new ActivityTransition.Builder().setActivityType(t).setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_ENTER).build());
            list.add(new ActivityTransition.Builder().setActivityType(t).setActivityTransition(ActivityTransition.ACTIVITY_TRANSITION_EXIT).build());
        }
        try {
            ActivityRecognition.getClient(ctx.getApplicationContext())
                .requestActivityTransitionUpdates(new ActivityTransitionRequest(list), pendingIntent(ctx))
                .addOnSuccessListener(v -> {
                    prefs(ctx).edit().putBoolean(KEY_ON, true).apply();
                    if (done != null) done.ok();
                })
                .addOnFailureListener(e -> {
                    if (done != null) done.fail("이동 감지를 시작하지 못했어요: " + e.getMessage());
                });
        } catch (SecurityException e) {
            if (done != null) done.fail("신체 활동 권한이 없어요");
        }
    }

    @SuppressWarnings("MissingPermission")
    static void stop(Context ctx) {
        prefs(ctx).edit().putBoolean(KEY_ON, false).apply();
        try {
            ActivityRecognition.getClient(ctx.getApplicationContext()).removeActivityTransitionUpdates(pendingIntent(ctx));
        } catch (Exception ignored) {}
    }

    static String name(int type) {
        switch (type) {
            case DetectedActivity.WALKING: return "walking";
            case DetectedActivity.RUNNING: return "running";
            case DetectedActivity.ON_BICYCLE: return "bicycle";
            case DetectedActivity.IN_VEHICLE: return "vehicle";
            case DetectedActivity.STILL: return "still";
            default: return null;
        }
    }

    static synchronized void append(Context ctx, long time, String activity, boolean enter) {
        SharedPreferences p = prefs(ctx);
        JSONArray old;
        try { old = new JSONArray(p.getString(KEY_LOG, "[]")); } catch (Exception e) { old = new JSONArray(); }
        JSONArray next = new JSONArray();
        long cutoff = System.currentTimeMillis() - KEEP_MS;
        int from = Math.max(0, old.length() - MAX_ENTRIES + 1);
        for (int i = from; i < old.length(); i++) {
            JSONObject o = old.optJSONObject(i);
            if (o != null && o.optLong("t") >= cutoff) next.put(o);
        }
        try {
            JSONObject o = new JSONObject();
            o.put("t", time);
            o.put("a", activity);
            o.put("k", enter ? "enter" : "exit");
            next.put(o);
        } catch (Exception ignored) {}
        p.edit().putString(KEY_LOG, next.toString()).apply();
    }

    static synchronized JSArray read(Context ctx, long start, long end) {
        JSArray out = new JSArray();
        try {
            JSONArray log = new JSONArray(prefs(ctx).getString(KEY_LOG, "[]"));
            for (int i = 0; i < log.length(); i++) {
                JSONObject o = log.optJSONObject(i);
                if (o == null) continue;
                long t = o.optLong("t");
                if (t < start || t > end) continue;
                JSObject j = new JSObject();
                j.put("time", t);
                j.put("activity", o.optString("a"));
                j.put("kind", o.optString("k"));
                out.put(j);
            }
        } catch (Exception ignored) {}
        return out;
    }
}
