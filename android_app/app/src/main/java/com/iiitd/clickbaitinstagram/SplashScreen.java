package com.iiitd.clickbaitinstagram;

import androidx.appcompat.app.AppCompatActivity;

import android.content.Intent;
import android.os.Bundle;
import android.os.Handler;
import android.view.WindowManager;

public class SplashScreen extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        getWindow().setFlags(WindowManager.LayoutParams.FLAG_FULLSCREEN, WindowManager.LayoutParams.FLAG_FULLSCREEN);
        setContentView(R.layout.activity_splash_screen);

        Handler handler = new Handler();
        int SPLASH_TIME = 1500;
        handler.postDelayed(new Runnable() {
            @Override
            public void run() {
                Intent intentHomeScreen = new Intent(SplashScreen.this, HomeScreen.class);
                startActivity(intentHomeScreen);
                finish();
            }
        }, SPLASH_TIME);

    }
}
