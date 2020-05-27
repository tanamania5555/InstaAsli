package com.iiitd.clickbaitinstagram;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.Service;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Color;
import android.os.Build;
import android.os.IBinder;
import android.util.Log;

import androidx.annotation.Nullable;
import androidx.core.app.NotificationCompat;

import java.util.Timer;
import java.util.TimerTask;

public class AutomaticService extends Service {

    private ClipboardManager mClipboardManager;
    private final int TIME_DELAY = 1000;
    private final int TIME_PERIOD = 1000;
    private Timer timer;
    private TimerTask timerTask;
    private Context context = null;
    private int counter = 0;

    @Nullable
    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    public AutomaticService(Context appContext){
        super();
        context = appContext;
        Log.d("TAG", "Automatic Service Constructor Called");
    }

    public AutomaticService(){
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {

        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O)
            startMyOwnForeground();
        else
            startForeground(1, new Notification());
        super.onStartCommand(intent, flags, startId);

        startTimer();
        mClipboardManager = (ClipboardManager) getSystemService(CLIPBOARD_SERVICE);
        mClipboardManager.addPrimaryClipChangedListener(mOnPrimaryClipChangedListener);

        return START_STICKY;
    }

    @Override
    public void onDestroy() {
        super.onDestroy();

        Log.d("TAG", "on destroy!");

        Intent broadcastIntent = new Intent("com.iiitd.clickbaitinstagram.restartService");
        sendBroadcast(broadcastIntent);
        stopTimerTask();

        if (mClipboardManager != null) {
            mClipboardManager.removePrimaryClipChangedListener(mOnPrimaryClipChangedListener);
        }
    }

    public void startTimer() {
        timer = new Timer();
        initializeTimerTask();
        timer.schedule(timerTask, TIME_DELAY, TIME_PERIOD);
    }

    public void initializeTimerTask() {
        timerTask = new TimerTask() {
            public void run() {
                Log.d("TAG", "in timer ++++  " + (counter++));
            }
        };
    }

    public void stopTimerTask() {
        if (timer != null) {
            timer.cancel();
            timer = null;
        }
    }

    private ClipboardManager.OnPrimaryClipChangedListener mOnPrimaryClipChangedListener =
            new ClipboardManager.OnPrimaryClipChangedListener() {
                @Override
                public void onPrimaryClipChanged() {

                    String charSequence = "EMPTY";
                    if(mClipboardManager.getPrimaryClip().getItemAt(0).getText() != null)
                        charSequence =  mClipboardManager.getPrimaryClip().getItemAt(0).getText().toString();
                    System.out.println("Copied Link : ====================" + charSequence);
                    Log.d("TAG", charSequence);
                    boolean isActivityStopped = HelperFunctions.isActivityRunning(getBaseContext(), HomeScreen.class);
//                    boolean isActivityStopped = isActivityRunning(HomeScreen.class);
                    boolean isInstLinkPossibility = HelperFunctions.isInstaLink(charSequence);

                    if(isInstLinkPossibility){
                        Intent homeScreenIntent = new Intent(getApplicationContext(), HomeScreen.class);
                        homeScreenIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                        homeScreenIntent.putExtra("LINK", charSequence);
                        startActivity(homeScreenIntent);
                    }
                }
            };


    private void startMyOwnForeground(){
        String NOTIFICATION_CHANNEL_ID = "com.iiitd.clickbaitinstagram";
        String channelName = "Automatic Service";
        NotificationChannel chan = new NotificationChannel(NOTIFICATION_CHANNEL_ID, channelName, NotificationManager.IMPORTANCE_NONE);
        chan.setLightColor(Color.BLUE);
        chan.setLockscreenVisibility(Notification.VISIBILITY_PRIVATE);
        NotificationManager manager = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
        assert manager != null;
        manager.createNotificationChannel(chan);

        NotificationCompat.Builder notificationBuilder = new NotificationCompat.Builder(this, NOTIFICATION_CHANNEL_ID);
        Notification notification = notificationBuilder.setOngoing(true)
                .setSmallIcon(R.drawable.ic_notification)
                .setContentTitle("Instagram Clickbait Detector is running in background")
                .setPriority(NotificationManager.IMPORTANCE_MIN)
                .setCategory(Notification.CATEGORY_SERVICE)
                .build();
        startForeground(2, notification);
    }

}

