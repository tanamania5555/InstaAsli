package com.iiitd.clickbaitinstagram;

import android.app.ActivityManager;
import android.app.AlertDialog;
import android.app.ProgressDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.TextView;

import com.app.adprogressbarlib.AdCircleProgress;

import java.util.List;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

public class HelperFunctions {

    public static void showMessage(Context context, String title, String Message) {
        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setCancelable(true);
        builder.setNeutralButton("Ok", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });
        builder.setTitle(title);
        builder.setMessage(Message);
        builder.show();
    }

    public static void customShowMessage(Context context, String title, String Message) {
        LayoutInflater inflater = (LayoutInflater) context.getSystemService(Context.LAYOUT_INFLATER_SERVICE);
        final View resultView = inflater.inflate(R.layout.result_popup, null);

        TextView tv_popUp = resultView.findViewById(R.id.tv_popUp);
        AdCircleProgress acp = resultView.findViewById(R.id.pb_result);
        float result = Float.parseFloat(Message);
        acp.setProgress(result);
        tv_popUp.setText(title);

        AlertDialog.Builder builder = new AlertDialog.Builder(context);
        builder.setCancelable(true);
        builder.setView(resultView);
        builder.setPositiveButton("Ok", new DialogInterface.OnClickListener() {
            @Override
            public void onClick(DialogInterface dialog, int which) {
                dialog.cancel();
            }
        });
        builder.show();
    }

    public static ProgressDialog loading(Context context){
        return ProgressDialog.show(context, "","Checking. Please wait...", true);
    }

    public static boolean isInstaLink(String link){
        String URL_REGEX = "^((https?|ftp)://|(www|ftp)\\.)?[a-z0-9-]+(\\.[a-z0-9-]+)+([/?].*)?$";
        String URL_INSTA = "instagram.com";

        Pattern p = Pattern.compile(URL_REGEX);
        Matcher m = p.matcher(link);
        String linkInsta = link.toLowerCase();
        boolean res = m.find() && linkInsta.contains(URL_INSTA);

        return res;
    }

    public static Boolean isActivityRunning(Context passedContext, Class activityClass) {
        ActivityManager activityManager = (ActivityManager) passedContext.getSystemService(Context.ACTIVITY_SERVICE);
        List<ActivityManager.RunningTaskInfo> tasks = activityManager.getRunningTasks(Integer.MAX_VALUE);

        for (ActivityManager.RunningTaskInfo task : tasks) {
            if (activityClass.getCanonicalName().equalsIgnoreCase(task.baseActivity.getClassName()))
                return true;
        }

        return false;
    }

    //NOT GOOD ENOUGH FOR NOW, NOT USED
    public static boolean isAppRunning(final Context context, final String packageName) {
        final ActivityManager activityManager = (ActivityManager) context.getSystemService(Context.ACTIVITY_SERVICE);
        final List<ActivityManager.RunningAppProcessInfo> procInfos = activityManager.getRunningAppProcesses();
        if (procInfos != null)
        {
            for (final ActivityManager.RunningAppProcessInfo processInfo : procInfos) {
                if (processInfo.processName.equals(packageName)) {
                    return true;
                }
            }
        }
        return false;
    }

}
