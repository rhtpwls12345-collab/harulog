package com.harulog.app;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;

/** 휴대폰을 다시 켜면 활동 인식 등록이 풀리므로, 사용자가 켜 둔 경우 다시 등록한다. */
public class BootReceiver extends BroadcastReceiver {
    @Override
    public void onReceive(Context context, Intent intent) {
        if (intent == null) return;
        String act = intent.getAction();
        if (!Intent.ACTION_BOOT_COMPLETED.equals(act) && !Intent.ACTION_MY_PACKAGE_REPLACED.equals(act)) return;
        if (TransitionTracker.isEnabled(context)) TransitionTracker.start(context, null);
    }
}
