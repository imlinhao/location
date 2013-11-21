package com.wifi.getrssi;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileWriter;
import java.io.IOException;
import java.util.List;
import java.util.Timer;
import java.util.TimerTask;

import android.net.wifi.ScanResult;
import android.os.Bundle;
import android.os.Environment;
import android.app.Activity;
import android.view.Menu;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class Second extends Activity {
	Timer timer=new Timer(true);
	private WifiAdmin mWifiAdmin;
	//获取经纬度
	private EditText editText1,editText2;
	//获取button
	Button button1,button2,button3;
	// 扫描结果列表
	private List<ScanResult> list;
	private ScanResult mScanResult;
	 private StringBuffer sb=new StringBuffer(); 
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_second);
		mWifiAdmin = new WifiAdmin(this); 
		init();
	}


	private void init() {
		// TODO Auto-generated method stub
		editText1=(EditText)findViewById(R.id.editText1);
		editText2=(EditText)findViewById(R.id.editText2);
		button1=(Button)findViewById(R.id.button1);
		button2=(Button)findViewById(R.id.button2);
		button3=(Button)findViewById(R.id.button3);
		
		button1.setOnClickListener(new MyListener());//开始扫描记录
		button2.setOnClickListener(new MyListener());//结束wifi
		button3.setOnClickListener(new MyListener());//重新记录
	}
	
	private class MyListener implements OnClickListener{

		@Override
		public void onClick(View v) {
			// TODO Auto-generated method stub
			switch(v.getId())
			{
			case R.id.button1://开始扫描并记录成文件
				mWifiAdmin.openWifi();  
                Toast.makeText(getApplicationContext(), "当前wifi状态为："+mWifiAdmin.checkState(), 1).show();
                
                timer.schedule(new TimerTask() {
					
					@Override
					public void run() {
						// TODO Auto-generated method stub
						getAllNetWorkList();//记录并且保存到sd卡中去
					}
				}, 0, 500);
                
                break;
			case R.id.button2://结束wifi
				mWifiAdmin.closeWifi();  
                Toast.makeText(getApplicationContext(), "当前wifi状态为："+mWifiAdmin.checkState(), 1).show();
                break;
			case R.id.button3://删除原始文件
				deletFile();
				break;
			 default:  
	            break; 
			}
		}
		
	}

	public void getAllNetWorkList() {
		// TODO Auto-generated method stub
		//获取经纬度
		String lon=editText1.getText().toString();
		String lat=editText2.getText().toString();
		// 每次点击扫描之前清空上一次的扫描结果    
        if(sb!=null){  
            sb=new StringBuffer();  
        }  
        //开始扫描wifi
        mWifiAdmin.startScan();
        list=mWifiAdmin.getWifiList();
        if(list!=null){
        	sb.append(lon+","+lat+";");
            for(int i=0;i<list.size();i++){  
                //得到扫描结果  
                mScanResult=list.get(i);  
                sb=sb.append(mScanResult.BSSID+",").append(mScanResult.level+";");  
            }
            sb.append("\n");
        }
        //存入sd卡,文件名scan.txt
        try{
        	File f = new File(Environment.getExternalStorageDirectory()+"/scan.txt");
        	if(!f.exists())
        	{
        		f.createNewFile();
        	}
        	FileWriter os=new FileWriter(f, true);
        	os.write(sb.toString());
            os.close();
        }catch(IOException e)
        {
        	e.printStackTrace();
        }
	}


	public void deletFile() {
		// TODO Auto-generated method stub
		File f = new File(Environment.getExternalStorageDirectory()+"/scan.txt");
		if(f.exists())
		{
			f.delete();
		}
	}

}
