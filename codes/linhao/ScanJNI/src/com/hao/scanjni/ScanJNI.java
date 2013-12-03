package com.hao.scanjni;
import android.app.Activity;
import android.os.Bundle;
import android.net.wifi.WifiManager;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.content.IntentFilter;
import java.io.DataOutputStream;
import android.widget.Toast;
import android.util.Log;

public class ScanJNI extends Activity
{
	WifiManager mWifiManager;
	BroadcastReceiver mReceiver;
	IntentFilter mFilter;
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
		//init();
		//executeAsRoot();
		try{ 
			Process process = Runtime.getRuntime().exec("su");
			DataOutputStream out = new DataOutputStream(process.getOutputStream());
			out.writeBytes("mount -o remount rw /system\n");
			out.writeBytes("mv /system/file.old /system/file.new\n");
			out.writeBytes("ls / > /system/ls.txt\n");
			out.writeBytes("ls / > /sdcard/ls.txt\n");
			//out.writeBytes("hao > /sdcard/haoscan.txt\n  iw dev wlan0 freq 2412 2437 2452 >> /sdcard");
			out.writeBytes("exit\n");  
			out.flush();
			process.waitFor();
		}catch(Exception e){
		}
		setContentView(R.layout.main);
		//Thread t = new Thread(new Runnable(){
		//	public void run(){
		//		//scan(); //it sames send NL80211_TRIGGER_SCAN need root privalledge, so just work around it using executable binary
		//		//ref:http://stackoverflow.com/questions/10203927/grant-the-root-privilege-to-the-application

		//		executeAsRoot();
		//	}
		//});
		//t.start();
    }

void executeAsRoot()
{
    Process chperm;
    try {
		Log.d("scanjni","before su");
		chperm=Runtime.getRuntime().exec("su");
		Log.d("scanjni","after su");
		DataOutputStream os = new DataOutputStream(chperm.getOutputStream());
		//for(int i=0; i<100000;++i){
		//	os.writeBytes("/system/bin/hao > /sdcard/haoscan.txt\n");
		//	os.flush();
		//}

		Log.d("scanjni","before ls");
		os.writeBytes("ls / > /sdcard/ls.txt\n");
		os.flush();
		Log.d("scanjni","after ls");
		os.writeBytes("hao > /sdcard/haoscan.txt\n");
		os.flush();
		os.writeBytes("exit\n");
		os.flush();
		Log.d("scanjni","before waitfor");
		chperm.waitFor();
		Log.d("scanjni","after waitfor");

    } catch (Exception e) {
		Log.d("scanjni","Exception");
		Toast.makeText(ScanJNI.this,"Exception",Toast.LENGTH_SHORT).show();
    }
		Log.d("scanjni","Done");
		Toast.makeText(ScanJNI.this,"Done",Toast.LENGTH_SHORT).show();
}
	

    @Override
	public void onDestroy(){
		//cleanup();
		super.onDestroy();
	}
    //public native int init();
    //public native int scan();
    //public native int cleanup();
    //static{
    //	System.loadLibrary("nl-3");
    //	System.loadLibrary("nl-genl-3");
    //	System.loadLibrary("hao");
    //}
}
