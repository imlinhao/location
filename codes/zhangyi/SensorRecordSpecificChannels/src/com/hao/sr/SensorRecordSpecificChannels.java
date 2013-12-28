package com.hao.sr;

import android.app.Activity;
import android.os.Bundle;
import android.location.LocationListener;
import android.location.Location;
import android.location.LocationManager;
import android.content.Intent;
import android.content.Context;
import android.content.IntentFilter;
import android.provider.Settings;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.Toast;
import android.widget.ToggleButton;
import android.hardware.SensorEventListener;
import android.hardware.Sensor;
import android.hardware.SensorEvent;
import android.hardware.SensorManager;
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
import java.io.FileOutputStream;
import android.os.Environment;
import java.util.Calendar;
import java.io.DataOutputStream;
import java.io.File;
import java.io.BufferedWriter;
import java.io.FileWriter;
import java.io.IOException;

import android.os.PowerManager;
import android.content.BroadcastReceiver;
import android.os.Build;
import android.net.wifi.ScanResult;
import android.net.wifi.WifiInfo;
import android.net.wifi.WifiManager;
import java.util.List;
import android.annotation.TargetApi;
import android.widget.TextView;

public class SensorRecordSpecificChannels extends Activity
{
	private static final String  TAG = "WRITE_TO_SDCARD----->";
	
	static final int SAMPLERATE = 8000;
	static final int CHANNELS = AudioFormat.CHANNEL_IN_MONO;
	static final int AUDIO_ENCODING = AudioFormat.ENCODING_PCM_16BIT;
	AudioRecord mRecorder;
	Thread mRecordingThread;
	Thread mJNIThread;
	boolean mIsRecording = false;
	boolean mIsscanJNI = false;
	LocationManager mLocationManager;
	LocationListener mLocationListener = new MyLocationListener();
	SensorManager mSensorManager;
	SensorEventListener mSensorEventListener = new MySensorEventListener();
	Sensor mAcc, mMf, mGyro, mHum, mTemp, mLight, mPress, mProx, mLacc;
	String mSdcardPath;
	String DATADIR = "sensorrecord";
	String mTimeDir;
	String mTimePath;
	String AUDIO_FILENAME = "voice8k16bitmono.pcm"; //new file in the record thread
	String PHONEINFO_FILENAME = "phoneinfo.txt";
	String WIFI_FILENAME = "wifi.txt";
	String GPS_FILENAME = "gps.txt";
	String ACC_FILENAME = "acc.txt";
	String MF_FILENAME = "mf.txt";
	String GYRO_FILENAME = "gyro.txt";
	String HUM_FILENAME = "hum.txt";
	String TEMP_FILENAME = "temp.txt";
	String LIGHT_FILENAME = "light.txt";
	String PRESS_FILENAME = "press.txt";
	String PROX_FILENAME = "prox.txt";
	String LACC_FILENAME = "lacc.txt";
	
	String JNI_FILENAME = "scanJNI.txt";
	String GETJNI_FILENAME = "getscanJNI.txt";
	String VOICETIME_FILENAME="voicetime.txt";
	String STILLTIME_FILENAME="stilltime.txt";
	String MOVETIME_FILENAME="movetime.txt";
	String LOG_FILENAME = "log.txt";
	
	
	BufferedWriter mVoiceBW;
	BufferedWriter mStillBW;
	BufferedWriter mMoveBW;
	BufferedWriter mLogBW;
	BufferedWriter mJNIBW;
	
	BufferedWriter mPhoneinfoBW;
	BufferedWriter mWifiBW;
	BufferedWriter mGpsBW;
	BufferedWriter mAccBW;
	BufferedWriter mMfBW;
	BufferedWriter mGyroBW;
	BufferedWriter mHumBW;
	BufferedWriter mTempBW;
	BufferedWriter mLightBW;
	BufferedWriter mPressBW;
	BufferedWriter mProxBW;
	BufferedWriter mLaccBW;
	PowerManager mPm;
	PowerManager.WakeLock mWakeLock;
	WifiManager mWifiManager;
	BroadcastReceiver mReceiver;
	IntentFilter mFilter;
	boolean mIsScanning = false;
	StringBuffer mScanResultsSB;
	StringBuffer mGpsSB;
	StringBuffer mAccSB;
	StringBuffer mMfSB;
	StringBuffer mGyroSB;
	StringBuffer mHumSB;
	StringBuffer mTempSB;
	StringBuffer mLightSB;
	StringBuffer mPressSB;
	StringBuffer mProxSB;
	StringBuffer mLaccSB;
	
	StringBuffer mVoiceSB;
	StringBuffer mStillSB;
	StringBuffer mMoveSB;
	StringBuffer mLogSB;
	StringBuffer mJNISB;
	
	boolean mOrigWifiState;
	int mGpsNum = 0;
	TextView tvGps;
	
	Button moveBtn;
	ToggleButton stillBtn;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.main);
		tvGps = (TextView) findViewById(R.id.tvGps);
		moveBtn = (Button) findViewById(R.id.btn);
		stillBtn = (ToggleButton) findViewById(R.id.togbtn);
		

		
		mPm = (PowerManager)getSystemService(POWER_SERVICE);
		mWakeLock = mPm.newWakeLock(PowerManager.SCREEN_DIM_WAKE_LOCK,"SensorRecordSpecificChannels");
		mWakeLock.acquire();
		mWifiManager = (WifiManager)getSystemService(WIFI_SERVICE);
		mOrigWifiState = mWifiManager.isWifiEnabled();
		mWifiManager.setWifiEnabled(true);
		mReceiver = new BroadcastReceiver(){
			@Override
			public void onReceive(Context context, Intent intent){
				if(mIsScanning){
					saveScanResults();
//					mWifiManager.startScan();
				}
			}
		};
		mFilter = new IntentFilter(WifiManager.SCAN_RESULTS_AVAILABLE_ACTION);
		registerReceiver(mReceiver, mFilter);
		mScanResultsSB = new StringBuffer(256);
		mGpsSB = new StringBuffer(256);
		mAccSB = new StringBuffer(256);
		mMfSB = new StringBuffer(256);
		mGyroSB = new StringBuffer(256);
		mHumSB = new StringBuffer(256);
		mTempSB = new StringBuffer(256);
		mLightSB = new StringBuffer(256);
		mPressSB = new StringBuffer(256);
		mProxSB = new StringBuffer(256);
		mLaccSB = new StringBuffer(256);
		mVoiceSB = new StringBuffer(256);
		mStillSB = new StringBuffer(256);
		mMoveSB = new StringBuffer(256);
		mLogSB = new StringBuffer(256);
		mJNISB = new StringBuffer(256);

		Calendar c = Calendar.getInstance();	
		mTimeDir = c.get(Calendar.YEAR)+"_"+(c.get(Calendar.MONTH)+1)+"_"
			+c.get(Calendar.DAY_OF_MONTH)+"_"+c.get(Calendar.HOUR_OF_DAY)+"_"
			+c.get(Calendar.MINUTE)+"_"+c.get(Calendar.SECOND);
		if(Environment.MEDIA_MOUNTED.equals(Environment.getExternalStorageState())){
			mSdcardPath = Environment.getExternalStorageDirectory().getAbsolutePath();
		}else{
			Toast.makeText(SensorRecordSpecificChannels.this,"Please insert SDCARD",Toast.LENGTH_SHORT).show();
			mSdcardPath = "/sdcard"; //TODO:need more good way to handle sdcard exception
		}
		mTimePath = mSdcardPath+"/"+DATADIR+"/"+mTimeDir;
		File timePath = new File(mTimePath);
		if(!timePath.exists()) timePath.mkdirs();

		mLocationManager = (LocationManager)getSystemService(LOCATION_SERVICE);
		mLocationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER,0,0f,mLocationListener);
		mSensorManager = (SensorManager)getSystemService(SENSOR_SERVICE);
		mAcc = mSensorManager.getDefaultSensor(Sensor.TYPE_ACCELEROMETER);
		mMf = mSensorManager.getDefaultSensor(Sensor.TYPE_MAGNETIC_FIELD);
		mGyro = mSensorManager.getDefaultSensor(Sensor.TYPE_GYROSCOPE);
		mHum = mSensorManager.getDefaultSensor(Sensor.TYPE_RELATIVE_HUMIDITY);
		mTemp = mSensorManager.getDefaultSensor(Sensor.TYPE_TEMPERATURE);
		mLight = mSensorManager.getDefaultSensor(Sensor.TYPE_LIGHT);
		mPress = mSensorManager.getDefaultSensor(Sensor.TYPE_PRESSURE);
		mProx = mSensorManager.getDefaultSensor(Sensor.TYPE_PROXIMITY);
		mLacc = mSensorManager.getDefaultSensor(Sensor.TYPE_LINEAR_ACCELERATION);
		if(null!=mAcc) mSensorManager.registerListener(mSensorEventListener,mAcc,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mMf) mSensorManager.registerListener(mSensorEventListener,mMf,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mGyro) mSensorManager.registerListener(mSensorEventListener,mGyro,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mHum) mSensorManager.registerListener(mSensorEventListener,mHum,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mTemp) mSensorManager.registerListener(mSensorEventListener,mTemp,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mLight) mSensorManager.registerListener(mSensorEventListener,mLight,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mPress) mSensorManager.registerListener(mSensorEventListener,mPress,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mProx) mSensorManager.registerListener(mSensorEventListener,mProx,SensorManager.SENSOR_DELAY_FASTEST);
		if(null!=mLacc) mSensorManager.registerListener(mSensorEventListener,mLacc,SensorManager.SENSOR_DELAY_FASTEST);
		File phoneinfoFile = new File(mTimePath+"/"+PHONEINFO_FILENAME);
		File wifiFile = new File(mTimePath+"/"+WIFI_FILENAME);
		File gpsFile = new File(mTimePath+"/"+GPS_FILENAME);
		File accFile = new File(mTimePath+"/"+ACC_FILENAME);
		File mfFile = new File(mTimePath+"/"+MF_FILENAME);
		File gyroFile = new File(mTimePath+"/"+GYRO_FILENAME);
		File humFile = new File(mTimePath+"/"+HUM_FILENAME);
		File tempFile = new File(mTimePath+"/"+TEMP_FILENAME);
		File lightFile = new File(mTimePath+"/"+LIGHT_FILENAME);
		File pressFile = new File(mTimePath+"/"+PRESS_FILENAME);
		File proxFile = new File(mTimePath+"/"+PROX_FILENAME);
		File laccFile = new File(mTimePath+"/"+LACC_FILENAME);
		
		File JNIFile = new File(mTimePath+"/"+JNI_FILENAME);
		File voiceFile = new File(mTimePath+"/"+VOICETIME_FILENAME);
		File stillFile = new File(mTimePath+"/"+STILLTIME_FILENAME);
		File moveFile = new File(mTimePath+"/"+MOVETIME_FILENAME);
		File logFile = new File(mTimePath+"/"+LOG_FILENAME);
		try{
			if(!phoneinfoFile.exists()){phoneinfoFile.createNewFile();}
			if(!wifiFile.exists()){wifiFile.createNewFile();}
			if(!gpsFile.exists()){gpsFile.createNewFile();}
			if(!accFile.exists()){accFile.createNewFile();}
			if(!mfFile.exists()){mfFile.createNewFile();}
			if(!gyroFile.exists()){gyroFile.createNewFile();}
			if(!humFile.exists()){humFile.createNewFile();}
			if(!tempFile.exists()){tempFile.createNewFile();}
			if(!lightFile.exists()){lightFile.createNewFile();}
			if(!pressFile.exists()){pressFile.createNewFile();}
			if(!proxFile.exists()){proxFile.createNewFile();}
			if(!laccFile.exists()){laccFile.createNewFile();}
			
			if(!JNIFile.exists()){JNIFile.createNewFile();}
			if(!voiceFile.exists()){voiceFile.createNewFile();}
			if(!stillFile.exists()){stillFile.createNewFile();}
			if(!moveFile.exists()){moveFile.createNewFile();}
			if(!logFile.exists()){logFile.createNewFile();}
			
			mPhoneinfoBW = new BufferedWriter(new FileWriter(phoneinfoFile));
			mWifiBW = new BufferedWriter(new FileWriter(wifiFile));
			mGpsBW = new BufferedWriter(new FileWriter(gpsFile));
			mAccBW = new BufferedWriter(new FileWriter(accFile));
			mMfBW = new BufferedWriter(new FileWriter(mfFile));
			mGyroBW = new BufferedWriter(new FileWriter(gyroFile));
			mHumBW = new BufferedWriter(new FileWriter(humFile));
			mTempBW = new BufferedWriter(new FileWriter(tempFile));
			mLightBW = new BufferedWriter(new FileWriter(lightFile));
			mPressBW = new BufferedWriter(new FileWriter(pressFile));
			mProxBW = new BufferedWriter(new FileWriter(proxFile));
			mLaccBW = new BufferedWriter(new FileWriter(laccFile));
			
			mJNIBW = new BufferedWriter(new FileWriter(JNIFile));
			mVoiceBW = new BufferedWriter(new FileWriter(voiceFile));
			mStillBW = new BufferedWriter(new FileWriter(stillFile));
			mMoveBW = new BufferedWriter(new FileWriter(moveFile));
			mLogBW = new BufferedWriter(new FileWriter(logFile));
		}catch(Exception e){
			e.printStackTrace();
		}

		try{
			WifiManager wifi = (WifiManager) getSystemService(Context.WIFI_SERVICE);  
	        WifiInfo info = wifi.getConnectionInfo();
	        String phonemac = info.getMacAddress();
			StringBuffer phoneinfoSB = new StringBuffer(256);
			phoneinfoSB.append("VERSION.SDK_INT:").append(Build.VERSION.SDK_INT).append("\nMANUFACTUERE:").append(Build.MANUFACTURER).append("\nMODEL:").append(Build.MODEL).append("\nPRODUCT:").append(Build.PRODUCT).append("\nDEVICE:").append(Build.DEVICE).append("\nCPU_ABI:").append(Build.CPU_ABI).append("\nCPU_ABI2:").append(Build.CPU_ABI2).append("\nMACINFO:").append(phonemac);
			mPhoneinfoBW.write(phoneinfoSB.toString());
			mPhoneinfoBW.flush();
			mPhoneinfoBW.close();
		}catch(Exception e){
		}

		mIsScanning = true;
//		mWifiManager.startScan();
		startRecording();
		
		scanJNI();
    }

	public void moveRecord(View v)
	{
		try{
			Log.d(TAG, "moveRecode---start record");
			mLogBW.write("moveRecode---start record"+"\n");
			mMoveBW.write(System.currentTimeMillis()+"\n");
			mMoveBW.flush();
			Log.d(TAG, "moveRecode---finish record"+System.currentTimeMillis());
			mLogBW.write("moveRecode---finish record"+"\n");
		}catch(Exception e)
		{
			Log.d(TAG, "moveRecode---record error");
			try{
				mLogBW.write("moveRecode---record error"+"\n");
			}catch(Exception e1){
				e1.printStackTrace();
			}
			
			Toast.makeText(SensorRecordSpecificChannels.this,"StillRecord Error",Toast.LENGTH_SHORT).show();
		}
		
	}
	
	public void stillRecord(View v)
	{
		try{
			if(stillBtn.isChecked())
			{
				Log.d(TAG, "stillRecord---start record");
				mLogBW.write("stillRecord---start record"+"\n");
				mStillBW.write(System.currentTimeMillis()+"\n");
				mStillBW.flush();
				Log.d(TAG, "stillRecord---finish record"+System.currentTimeMillis());
				mLogBW.write("stillRecord---finish record"+"\n");
			}else{
				Log.d(TAG, "stillRecord---start record");
				mLogBW.write("stillRecord---start record"+"\n");
				mStillBW.write(System.currentTimeMillis()+"\n");
				mStillBW.flush();
				Log.d(TAG, "stillRecord---finish record"+System.currentTimeMillis());
				mLogBW.write("stillRecord---finish record"+"\n");
			}
		} catch(Exception e){
			Log.d(TAG, "stillRecord---record error");
			try{
				mLogBW.write("stillRecord---record error"+"\n");
			}catch(Exception e1)
			{
				e1.printStackTrace();
			}
			
			Toast.makeText(SensorRecordSpecificChannels.this,"StillRecord Error",Toast.LENGTH_SHORT).show();
		}
	}
	@Override
	public void onDestroy(){
		mIsScanning = false;
		mIsscanJNI = false;
		mJNIThread = null;
		unregisterReceiver(mReceiver);
		mWakeLock.release();
		mWifiManager.setWifiEnabled(mOrigWifiState);

		mLocationManager.removeUpdates(mLocationListener);
		mSensorManager.unregisterListener(mSensorEventListener);
		if(null!=mRecorder){
			mIsRecording = false;
			mRecorder.stop();
			mRecorder.release();
			mRecorder = null;
			mRecordingThread = null;
		}
		try{
			mWifiBW.flush();
			mGpsBW.flush();
			mAccBW.flush();
			mMfBW.flush();
			mGyroBW.flush();
			mHumBW.flush();
			mTempBW.flush();
			mLightBW.flush();
			mPressBW.flush();
			mProxBW.flush();
			mLaccBW.flush();
			mVoiceBW.flush();
			mStillBW.flush();
			mMoveBW.flush();
			mLogBW.flush();
//			mJNIBW.flush();

			mWifiBW.close();
			mGpsBW.close();
			mAccBW.close();
			mMfBW.close();
			mGyroBW.close();
			mHumBW.close();
			mTempBW.close();
			mLightBW.close();
			mPressBW.close();
			mProxBW.close();
			mLaccBW.close();
			mVoiceBW.close();
//			mJNIBW.close();
			mStillBW.close();
			mMoveBW.close();
			Log.d(TAG, "AllRecorded---finish record");
			mLogBW.write("AllRecorded---finish record"+"\n");
			
			mLogBW.close();
			Toast.makeText(SensorRecordSpecificChannels.this,"All Done",Toast.LENGTH_SHORT).show();
		}catch(Exception e){
			Log.d(TAG, "AllRecord---record ERROR");
			try{
				mLogBW.write("AllRecord---record ERROR"+"\n");
				mLogBW.close();
			}catch(Exception e1){
				e1.printStackTrace();
			}
			
			Toast.makeText(SensorRecordSpecificChannels.this,"Exception",Toast.LENGTH_SHORT).show();
			e.printStackTrace();
		}
		
		super.onDestroy();
	}

	class MyLocationListener implements LocationListener{
		@Override
		public void onLocationChanged(Location location){
			//Toast.makeText(SensorRecordSpecificChannels.this,"Get Location",Toast.LENGTH_SHORT).show();
			mGpsSB.setLength(0);
			mGpsSB.append(System.currentTimeMillis()+";");
			mGpsSB.append(location.getLongitude()+";");
			mGpsSB.append(location.getLatitude()+";");
			mGpsSB.append(location.getAltitude()+";");
			mGpsSB.append(location.getAccuracy()+";");
			mGpsSB.append(location.getTime()+"\n");
			//Toast.makeText(SensorRecordSpecificChannels.this,mGpsSB.toString(),Toast.LENGTH_SHORT).show();
			++mGpsNum;
			tvGps.setText("GpsNum: "+mGpsNum+"\n"+mGpsSB.toString());
			try{
				mGpsBW.write(mGpsSB.toString());
			}catch(Exception e){
			}
		}

		@Override
		public void onProviderDisabled(String provider){
			Toast.makeText(SensorRecordSpecificChannels.this,"Please open GPS",Toast.LENGTH_SHORT).show();
			Intent intent = new Intent(Settings.ACTION_LOCATION_SOURCE_SETTINGS);
			startActivity(intent);
		}

		@Override
		public void onProviderEnabled(String provider){
		}

		@Override
		public void onStatusChanged(String provider, int status, Bundle extra){
		}
	}

	class MySensorEventListener implements SensorEventListener{
		@Override
		public void onAccuracyChanged(Sensor sensor, int accuracy){
		}

		@Override
		public void onSensorChanged(SensorEvent event){
			if(event.sensor.getType()==Sensor.TYPE_ACCELEROMETER){
				mAccSB.setLength(0);
				mAccSB.append(System.currentTimeMillis()+";");
				mAccSB.append(event.values[0]+";");
				mAccSB.append(event.values[1]+";");
				mAccSB.append(event.values[2]+";");
				mAccSB.append(event.timestamp+"\n");
				try{
					mAccBW.write(mAccSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_MAGNETIC_FIELD){
				mMfSB.setLength(0);
				mMfSB.append(System.currentTimeMillis()+";");
				mMfSB.append(event.values[0]+";");
				mMfSB.append(event.values[1]+";");
				mMfSB.append(event.values[2]+";");
				mMfSB.append(event.timestamp+"\n");
				try{
					mMfBW.write(mMfSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_GYROSCOPE){
				mGyroSB.setLength(0);
				mGyroSB.append(System.currentTimeMillis()+";");
				mGyroSB.append(event.values[0]+";");
				mGyroSB.append(event.values[1]+";");
				mGyroSB.append(event.values[2]+";");
				mGyroSB.append(event.timestamp+"\n");
				try{
					mGyroBW.write(mGyroSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_RELATIVE_HUMIDITY){
				mHumSB.setLength(0);
				mHumSB.append(System.currentTimeMillis()+";");
				mHumSB.append(event.values[0]+";");
				mHumSB.append(event.timestamp+"\n");
				try{
					mHumBW.write(mHumSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_AMBIENT_TEMPERATURE){
				mTempSB.setLength(0);
				mTempSB.append(System.currentTimeMillis()+";");
				mTempSB.append(event.values[0]+";");
				mTempSB.append(event.timestamp+"\n");
				try{
					mTempBW.write(mTempSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_LIGHT){
				mLightSB.setLength(0);
				mLightSB.append(System.currentTimeMillis()+";");
				mLightSB.append(event.values[0]+";");
				mLightSB.append(event.timestamp+"\n");
				try{
					mLightBW.write(mLightSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_PRESSURE){
				mPressSB.setLength(0);
				mPressSB.append(System.currentTimeMillis()+";");
				mPressSB.append(event.values[0]+";");
				mPressSB.append(event.timestamp+"\n");
				try{
					mPressBW.write(mPressSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_PROXIMITY){
				mProxSB.setLength(0);
				mProxSB.append(System.currentTimeMillis()+";");
				mProxSB.append(event.values[0]+";");
				mProxSB.append(event.timestamp+"\n");
				try{
					mProxBW.write(mProxSB.toString());
				}catch(Exception e){
				}
			}
			if(event.sensor.getType()==Sensor.TYPE_LINEAR_ACCELERATION){
				mLaccSB.setLength(0);
				mLaccSB.append(System.currentTimeMillis()+";");
				mLaccSB.append(event.values[0]+";");
				mLaccSB.append(event.values[1]+";");
				mLaccSB.append(event.values[2]+";");
				mLaccSB.append(event.timestamp+"\n");
				try{
					mLaccBW.write(mLaccSB.toString());
				}catch(Exception e){
				}
			}
		}
	}

	int bufferElements2Rec = 1024; // want to play 2048 (2K) since 2 bytes we use only 1024
	int bytesPerElement = 2; // 2 bytes in 16bit format

	void startRecording(){
		mRecorder = new AudioRecord(MediaRecorder.AudioSource.MIC,SAMPLERATE,CHANNELS,AUDIO_ENCODING,bufferElements2Rec*bytesPerElement);
		mRecorder.startRecording();
		mIsRecording = true;
		mRecordingThread = new Thread(new Runnable(){
			public void run(){
				writeAudioDataToFile();
			}
		}, "AudioRecorder Thread");
		mRecordingThread.start();
	}

	byte[] short2byte(short[] sData){
		int shortArrsize = sData.length;
		byte[] bytes = new byte[shortArrsize*2];
		for(int i=0; i<shortArrsize; ++i){
			bytes[i*2] = (byte)(sData[i]&0x00FF);
			bytes[(i*2)+1]=(byte)(sData[i]>>8);
			sData[i]=0;
		}
		return bytes;
	}

	void writeAudioDataToFile(){
		try{
			Log.d(TAG, "firstvoiceRecord---start record");
			mLogBW.write("firstvoiceRecord---start record"+"\n");
			mVoiceBW.write(System.currentTimeMillis()+"\n");
			mVoiceBW.flush();
			Log.d(TAG, "firstvoiceRecord---finish record"+System.currentTimeMillis());
			mLogBW.write("firstvoiceRecord---finish record"+"\n");
		}catch(Exception e)
		{
			Log.d(TAG, "firstvoiceRecord---record ERROR");
			try{
				mLogBW.write("firstvoiceRecord---record ERROR"+"\n");
			}catch(Exception e1){
				e1.printStackTrace();
			}
			
			e.printStackTrace();
		}
		
		String filePath = mTimePath+"/"+AUDIO_FILENAME;
		short sData[] = new short[bufferElements2Rec];
		FileOutputStream os = null;
		try{
			os = new FileOutputStream(filePath);
		}catch(Exception e){
			e.printStackTrace();
		}
		while(mIsRecording){
			mRecorder.read(sData,0,bufferElements2Rec);
			try{
				byte bData[] = short2byte(sData);
				os.write(bData,0,bufferElements2Rec*bytesPerElement);
			}catch(Exception e){
				e.printStackTrace();
			}
		}
		try{
			os.close();
			Log.d(TAG, "secondvoiceRecord---start record");
			mLogBW.write("secondvoiceRecord---start record"+"\n");
			mVoiceBW.write(System.currentTimeMillis()+"\n");
			Log.d(TAG, "secondvoiceRecord---finish record"+System.currentTimeMillis());
			mLogBW.write("secondvoiceRecord---finish record"+"\n");
		}catch(Exception e){
			e.printStackTrace();
		}
	}

	void scanJNI(){
		mIsscanJNI = true;
		mJNIThread = new Thread(new Runnable() {
			
			@Override
			public void run() {
				String filePath = mTimePath+"/"+GETJNI_FILENAME;
				File JNIFile = new File(mTimePath+"/"+JNI_FILENAME);
				if(!JNIFile.exists()){
					try {
						JNIFile.createNewFile();
					} catch (IOException e) {
					// TODO Auto-generated catch block
						e.printStackTrace();
					}
				}
				Process process = null;
				try {
					process = Runtime.getRuntime().exec("su");
				} catch (IOException e1) {
					// TODO Auto-generated catch block
					e1.printStackTrace();
				}
				DataOutputStream out = new DataOutputStream(process.getOutputStream());
				


				while(mIsscanJNI){
					try{
						out.writeBytes("iw dev wlan0 scan freq 2412 2437 2452 >> "+filePath+"\n");
						out.writeBytes("echo '\n' >> "+filePath+"\n");
						out.flush();		

					}catch(Exception e){
						e.printStackTrace();
					}
				}
				
				try {
					out.writeBytes("exit\n");
					out.flush();
					
				} catch (IOException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}  
				try {
					process.waitFor();
				} catch (InterruptedException e) {
					// TODO Auto-generated catch block
					e.printStackTrace();
				}
				
				
			}
		});
		mJNIThread.start();
		
	}
	
	@TargetApi(17)
	public void saveScanResults(){
		List<ScanResult> scanResults = mWifiManager.getScanResults();
		ScanResult scanResult;
		mScanResultsSB.setLength(0);
		mScanResultsSB.append(System.currentTimeMillis()+";");
		for(int i=0; i<scanResults.size(); ++i){
			scanResult = scanResults.get(i);
			mScanResultsSB.append(scanResult.frequency+",");
			mScanResultsSB.append(scanResult.SSID+",");
			mScanResultsSB.append(scanResult.BSSID+",");
			if(Build.VERSION.SDK_INT>=17){
				mScanResultsSB.append(scanResult.timestamp+","); //API Level 17
			}
			mScanResultsSB.append(scanResult.level+";");
		}
		try{
			mWifiBW.write(mScanResultsSB.append("\n").toString());
		}catch(Exception e){
		}
	}

}
