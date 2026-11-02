package com.harulog.app;

import android.app.AppOpsManager;
import android.app.usage.UsageEvents;
import android.app.usage.UsageStatsManager;
import android.content.Context;
import android.content.Intent;
import android.net.Uri;
import android.os.Build;
import android.os.Process;
import android.provider.Settings;

import com.getcapacitor.JSArray;
import com.getcapacitor.JSObject;
import com.getcapacitor.Plugin;
import com.getcapacitor.PluginCall;
import com.getcapacitor.PluginMethod;
import com.getcapacitor.annotation.CapacitorPlugin;

/**
 * 하루로그 PhoneSignals: 화면 켜짐·꺼짐 시각만 읽어 수면 추정에 쓴다.
 * 어떤 앱을 썼는지(패키지 이름)는 JS로 넘기지 않는다.
 * 필요 권한: PACKAGE_USAGE_STATS (설정 › 사용 정보 접근에서 사용자가 직접 허용)
 */
@CapacitorPlugin(name = "PhoneSignals")
public class PhoneSignalsPlugin extends Plugin {

    private boolean hasUsageAccess() {
        Context ctx = getContext();
        AppOpsManager ops = (AppOpsManager) ctx.getSystemService(Context.APP_OPS_SERVICE);
        if (ops == null) return false;
        int mode;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.Q) {
            mode = ops.unsafeCheckOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), ctx.getPackageName());
        } else {
            mode = ops.checkOpNoThrow(AppOpsManager.OPSTR_GET_USAGE_STATS, Process.myUid(), ctx.getPackageName());
        }
        return mode == AppOpsManager.MODE_ALLOWED;
    }

    @PluginMethod
    public void checkUsageAccess(PluginCall call) {
        JSObject ret = new JSObject();
        ret.put("granted", hasUsageAccess());
        ret.put("screenEventsSupported", Build.VERSION.SDK_INT >= Build.VERSION_CODES.P);
        call.resolve(ret);
    }

    @PluginMethod
    public void openUsageAccessSettings(PluginCall call) {
        Intent intent = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
        // Android 10+ 일부 기기는 앱별 화면으로 바로 열린다
        intent.setData(Uri.parse("package:" + getContext().getPackageName()));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        try {
            getContext().startActivity(intent);
        } catch (Exception e) {
            Intent fallback = new Intent(Settings.ACTION_USAGE_ACCESS_SETTINGS);
            fallback.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
            getContext().startActivity(fallback);
        }
        call.resolve();
    }

    /** { start: epochMs, end: epochMs } → { events: [{ time, type: 'on'|'off'|'unlock' }] } */
    @PluginMethod
    public void getScreenEvents(PluginCall call) {
        if (!hasUsageAccess()) {
            call.reject("사용 정보 접근 권한이 없어요", "NO_USAGE_ACCESS");
            return;
        }
        long now = System.currentTimeMillis();
        long end = Math.min(call.getLong("end", now), now);
        long start = call.getLong("start", end - 24L * 3600_000L);
        if (start >= end) {
            call.reject("start 가 end 보다 늦어요");
            return;
        }
        UsageStatsManager usm = (UsageStatsManager) getContext().getSystemService(Context.USAGE_STATS_SERVICE);
        JSArray out = new JSArray();
        if (usm != null) {
            UsageEvents events = usm.queryEvents(start, end);
            UsageEvents.Event e = new UsageEvents.Event();
            while (events != null && events.hasNextEvent()) {
                events.getNextEvent(e);
                String type = null;
                int t = e.getEventType();
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.P) {
                    if (t == UsageEvents.Event.SCREEN_INTERACTIVE) type = "on";
                    else if (t == UsageEvents.Event.SCREEN_NON_INTERACTIVE) type = "off";
                    else if (t == UsageEvents.Event.KEYGUARD_HIDDEN) type = "unlock";
                } else {
                    // Android 8 (API 26~27): 앱이 앞으로 나온 시각만 '켜짐'으로 근사
                    if (t == UsageEvents.Event.MOVE_TO_FOREGROUND) type = "on";
                    else if (t == UsageEvents.Event.MOVE_TO_BACKGROUND) type = "off";
                }
                if (type == null) continue;
                JSObject o = new JSObject();
                o.put("time", e.getTimeStamp());
                o.put("type", type);
                out.put(o);
            }
        }
        JSObject ret = new JSObject();
        ret.put("events", out);
        call.resolve(ret);
    }
}
