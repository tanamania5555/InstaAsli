package com.iiitd.clickbaitinstagram;

import android.app.ActivityManager;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.core.content.ContextCompat;

import com.android.volley.AuthFailureError;
import com.android.volley.DefaultRetryPolicy;
import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.VolleyError;
import com.android.volley.VolleyLog;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.UnsupportedEncodingException;
import java.util.regex.Matcher;
import java.util.regex.Pattern;


public class HomeScreen extends AppCompatActivity {

    ServiceRestartAutomaticReceiver receiver;
    private EditText et_link;
    private EditText et_user;
    private Button b_checkPost;
    private Button b_checkUser;
    private String link;
    private static final String URL_REGEX = "^((https?|ftp)://|(www|ftp)\\.)?[a-z0-9-]+(\\.[a-z0-9-]+)+([/?].*)?$";
    private static final String URL_INSTA = "instagram.com";

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home_screen);

        link = "";
        et_link = findViewById(R.id.et_link);
        b_checkPost = findViewById(R.id.b_checkPost);
        et_user = findViewById(R.id.et_user);
        b_checkUser = findViewById(R.id.b_checkUser);

        Bundle extras = getIntent().getExtras();
        if(extras != null){
            link = extras.getString("LINK");
            Log.d("TAGG", "HIHI = " + link);
            et_link.setText(link);
        }
        else{
            Log.d("TAGG", "NO EXTRAS");
        }

        IntentFilter filter = new IntentFilter();
        filter.addAction("com.iiitd.clickbaitinstagram.restartService");

        receiver = new ServiceRestartAutomaticReceiver();
        registerReceiver(receiver, filter);

        //Check Post Button
        b_checkPost.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!et_link.getText().toString().trim().isEmpty()){
                    link = et_link.getText().toString().trim();

                    //May need to modify this checking of URL
                    Pattern p = Pattern.compile(URL_REGEX);
                    Matcher m = p.matcher(link);
                    String linkInsta = link.toLowerCase();
                    if(m.find() && linkInsta.contains(URL_INSTA)) {
                        //Toast.makeText(HomeScreen.this, "WORKING", Toast.LENGTH_SHORT).show();

                        //TESTING
                        //HelperFunctions.customShowMessage(HomeScreen.this, "Result","75");
                        try {
                            sendToBackend(link,"post/");
                        } catch (JSONException e) {
                            e.printStackTrace();
                        }
                    }
                    else{
                        et_link.setError("Not an Instagram Link");
                    }

                }
                else{
                    et_link.setError("This field can't be empty");
                }
            }
        });

        //Check User Button, MODIFY THIS FUNCTION
        b_checkUser.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                if(!et_user.getText().toString().trim().isEmpty()){
                    link = et_user.getText().toString().trim();

                    // MODIFY BELOW FUNCTION AS PER "USER"
                    //May need to modify this checking of URL
                    Pattern p = Pattern.compile(URL_REGEX);
                    Matcher m = p.matcher(link);
                    String linkInsta = link.toLowerCase();
                        //Toast.makeText(HomeScreen.this, "WORKING", Toast.LENGTH_SHORT).show();
                    try {
                        sendToBackend(link,"user/");
                    } catch (JSONException e) {
                        e.printStackTrace();
                    }


                }
                else{
                    et_user.setError("This field can't be empty");
                }
            }
        });

        AutomaticService mSensorService = new AutomaticService(getApplicationContext());
        Intent mServiceIntent = new Intent(getApplicationContext(), mSensorService.getClass());
        if (!isMyServiceRunning(mSensorService.getClass())) {
            ContextCompat.startForegroundService(getApplicationContext(), mServiceIntent);
        }

    }

    private boolean isMyServiceRunning(Class<?> serviceClass) {
        ActivityManager manager = (ActivityManager) getSystemService(Context.ACTIVITY_SERVICE);
        for (ActivityManager.RunningServiceInfo service : manager.getRunningServices(Integer.MAX_VALUE)) {
            if (serviceClass.getName().equals(service.service.getClassName())) {
                Log.d ("TAG", true+"");
                return true;
            }
        }
        Log.i ("TAG", false+"");
        return false;
    }


    protected void onDestroy() {
        super.onDestroy();
        unregisterReceiver(receiver);
    }


    public void sendToBackend(final String link1, String api) throws JSONException {

        final ProgressDialog progressDialog = HelperFunctions.loading(HomeScreen.this);

        final RequestQueue queue = Volley.newRequestQueue(this);
        String url = "https://insta-asli.herokuapp.com/"+api;
        JSONObject jsonBody = new JSONObject();
        jsonBody.put("link", link);
        final String requestBody = jsonBody.toString();

        final StringRequest stringRequest = new StringRequest(Request.Method.POST, url, new Response.Listener<String>(){
            @Override
            public void onResponse(String response){
                //Toast.makeText(HomeScreen.this, response, Toast.LENGTH_SHORT).show();

                //STOP Loading Screen
                progressDialog.cancel();
                try {
                    JSONObject hello = new JSONObject(response);
                    HelperFunctions.customShowMessage(HomeScreen.this, "Result", hello.get("classifier_result").toString());
                    //OLD VERSION
//                    HelperFunctions.showMessage(HomeScreen.this, "Result", "Clickbait % = "+hello.get("classifier_result").toString());
                } catch (JSONException e) {
                    e.printStackTrace();
                }
                // Pass The Result as String, Last Parameter in HelperFunctions.showMessage(context, "Result", result);

            }
        }, new Response.ErrorListener(){
            @Override
            public void onErrorResponse(VolleyError error){
                //STOP Loading Screen
                progressDialog.cancel();
                Toast.makeText(HomeScreen.this, error.toString(), Toast.LENGTH_SHORT).show();
            }
        }){
            @Override
            public String getBodyContentType() {
                return "application/json; charset=utf-8";
            }
            @Override
            public byte[] getBody() throws AuthFailureError {
                try {
                    return requestBody == null ? null : requestBody.getBytes("utf-8");
                } catch (UnsupportedEncodingException uee) {
                    VolleyLog.wtf("Unsupported Encoding while trying to get the bytes of %s using %s", requestBody, "utf-8");
                    return null;
                }
            }
        };
        stringRequest.setRetryPolicy(new DefaultRetryPolicy(50000,
                1,
                1));
        queue.add(stringRequest);
    }
}
