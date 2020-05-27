package com.iiitd.clickbaitinstagram;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.os.Build;
import android.util.Log;

import androidx.annotation.RequiresApi;

public class ServiceRestartAutomaticReceiver extends BroadcastReceiver {
    @RequiresApi(api = Build.VERSION_CODES.O)
    @Override
    public void onReceive(Context context, Intent intent) {
        Log.d("TAG", "Service Stops! Oops!!!!");
        context.startForegroundService(new Intent(context, AutomaticService.class));
    }
}
