package com.harulog.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.SystemClock;

import com.google.android.gms.location.ActivityTransition;
import com.google.android.gms.location.ActivityTransitionEvent;
import com.google.android.gms.location.ActivityTransitionResult;

/** 구글 활동 인식이 보내 주는 전환 이벤트를 받아 기기 안에 저장한다. */
public class TransitionReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null || !ActivityTransitionResult.hasResult(intent)) return;
        ActivityTransitionResult result = ActivityTransitionResult.extractResult(intent);
        if (result == null) return;
        long nowWall = System.currentTimeMillis(), nowElapsed = SystemClock.elapsedRealtimeNanos();
        for (ActivityTransitionEvent e : result.getTransitionEvents()) {
            String a = TransitionTracker.name(e.getActivityType());
            if (a == null) continue;
            long wall = nowWall - (nowElapsed - e.getElapsedRealTimeNanos()) / 1_000_000L;
            TransitionTracker.append(context, wall, a, e.getTransitionType() == ActivityTransition.ACTIVITY_TRANSITION_ENTER);
        }
    }
}
