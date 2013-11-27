package com.wifi.getrssi;

import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.location.LocationProvider;
import android.os.Bundle;
import android.provider.Settings;
import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {
	//获取组件
	TextView textView1;
	Button button1,button2;
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);
		textView1=(TextView)findViewById(R.id.textView1);
		button1=(Button)findViewById(R.id.button1);
		button2=(Button)findViewById(R.id.button2);
		
		Criteria criteria=new Criteria();
		criteria.setAccuracy(Criteria.ACCURACY_FINE);
		
		//进行gps定位
		button1.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				//定义locationManage对象
				LocationManager locManager=(LocationManager)getSystemService(Context.LOCATION_SERVICE);
				//判断GPS是否正常启动
		        if(!locManager.isProviderEnabled(LocationManager.GPS_PROVIDER)){
		            Toast.makeText(MainActivity.this, "请开启GPS导航...", Toast.LENGTH_SHORT).show();
		            //返回开启GPS导航设置界面
		            Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);   
		            startActivityForResult(intent,0); 
		            return;
		        }
		     // 从GPS获取最近的最近的定位信息
				Location location=locManager.getLastKnownLocation(LocationManager.GPS_PROVIDER);
				updateView(location);
				// 设置每3秒获取一次GPS的定位信息
				locManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 3000, 10, locationListener);
			}
		});
		
		//执行收集数据时
		button2.setOnClickListener(new OnClickListener() {
			
			@Override
			public void onClick(View arg0) {
				// TODO Auto-generated method stub
				Intent intent = new Intent();
				intent.setClass(getApplicationContext(), Second.class);
				startActivity(intent);
			}
		});
		
	}
	
	
	private final LocationListener locationListener = new LocationListener() {
		
		@Override
		public void onStatusChanged(String provider, int status, Bundle extras) {
			// TODO Auto-generated method stub
			//GPS状态为可见时
			switch (status) {
            case LocationProvider.AVAILABLE:
            	Toast.makeText(MainActivity.this, "当前GPS状态为可见状态", Toast.LENGTH_SHORT).show();
                break;
            //GPS状态为服务区外时
            case LocationProvider.OUT_OF_SERVICE:
            	Toast.makeText(MainActivity.this, "当前GPS状态为服务区外状态", Toast.LENGTH_SHORT).show();
                break;
            //GPS状态为暂停服务时
            case LocationProvider.TEMPORARILY_UNAVAILABLE:
            	Toast.makeText(MainActivity.this, "当前GPS状态为暂停服务状态", Toast.LENGTH_SHORT).show();
                break;
        }
		}
		
		@Override
		public void onProviderEnabled(String provider) {
			// TODO Auto-generated method stub
			// 当GPS LocationProvider可用时，更新位置
			//updateView(locManager.getLastKnownLocation(provider));
		}
		
		@Override
		public void onProviderDisabled(String provider) {
			// TODO Auto-generated method stub
			updateView(null);
			
		}
		
		@Override
		public void onLocationChanged(Location location) {
			// TODO Auto-generated method stub
			// 当GPS定位信息发生改变时，更新位置
			updateView(location);
		}
	};
	
	
	// 更新EditText中显示的内容
		public void updateView(Location newLocation)
		{
			if (newLocation != null)
			{
				float s = newLocation.getAccuracy();//精确度
				String t=String.valueOf(s);
				Toast.makeText(MainActivity.this, "精确度是:"+t, Toast.LENGTH_SHORT).show();
				StringBuilder sb = new StringBuilder();
				sb.append("实时的位置信息：\n");
				sb.append("经度：");
				sb.append(newLocation.getLongitude());
				sb.append("\n纬度：");
				sb.append(newLocation.getLatitude());
				textView1.setText(sb.toString());
			}
			else
			{
				// 如果传入的Location对象为空则清空EditText
				textView1.setText("");
			}
		}

}
