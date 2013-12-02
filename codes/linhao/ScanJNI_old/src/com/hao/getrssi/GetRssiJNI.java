package com.hao.getrssi;

import android.app.Activity;
import android.os.Bundle;
import android.net.wifi.WifiManager;
import android.content.BroadcastReceiver;
import android.content.Intent;
import android.content.Context;
import android.content.IntentFilter;

public class GetRssiJNI extends Activity
{
	WifiManager mWifiManager;
	BroadcastReceiver mReceiver;
	IntentFilter mFilter;
    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
	mWifiManager = (WifiManager)getSystemService(WIFI_SERVICE);
	mReceiver = new BroadcastReceiver(){
		@Override
		public void onReceive(Context context, Intent intent){
			getRssi();
		}
	};
	mFilter = new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
	registerReceiver(mReceiver, mFilter);
	mWifiManager.startScan();
        setContentView(R.layout.main);
    }

    @Override
	public void onDestroy(){
		unregisterReceiver(mReceiver);
		super.onDestroy();
	}
    public native int getRssi();
    static{
    	System.loadLibrary("nl-3");
    	System.loadLibrary("nl-genl-3");
    	System.loadLibrary("hao");
    }
}
