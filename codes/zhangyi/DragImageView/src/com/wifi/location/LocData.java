package com.wifi.location;

import com.jj.drag.R;

import android.content.Context;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.graphics.Canvas;
import android.graphics.Matrix;
import android.graphics.Bitmap.Config;
import android.graphics.drawable.BitmapDrawable;
import android.util.AttributeSet;
import android.view.View;

public class LocData extends View{
	




	// 初始的图片资源
	private Bitmap bitmap1,bitmap2;
	// 位图宽和高
	private int width1, height1,width2,height2;
	// Matrix 实例
	private Matrix matrix = new Matrix();
	// 设置倾斜度
	private float sx = 0.0f;
	// 缩放比例
	private float scale = 1.0f;
	// 判断缩放还是旋转
	private boolean isScale = true;
	
	
	//经度
	public float lon=0;
	//维度
	public float lat=0;
	//记录位图
	public Bitmap canvasBitmap = Bitmap.createBitmap(1000, 1000,Config.ARGB_8888);
	
	private Canvas canvas = new Canvas(canvasBitmap);
	
	public LocData(Context context) {
		super(context);
		// TODO Auto-generated constructor stub
		bitmap1 = BitmapFactory.decodeResource(getResources(),R.drawable.leaf).copy(Bitmap.Config.ARGB_8888,true);
		this.setFocusable(true);
		this.canvas.drawBitmap(bitmap1,0,0,null);
	}
	
	public Bitmap DrawMap(float lon, float lat)
	{
		// 获得位图1,2
		bitmap1 = BitmapFactory.decodeResource(getResources(),R.drawable.leaf).copy(Bitmap.Config.ARGB_8888,true);
		bitmap2 = ((BitmapDrawable)getResources().getDrawable(R.drawable.icon_geo)).getBitmap();
		// 获得位图宽1,2
		width1 = bitmap1.getWidth(); 
		width2 = bitmap2.getWidth();
		// 获得位图高1,2
		height1 = bitmap1.getHeight();
		height2 = bitmap2.getHeight();
		// 使当前视图获得焦点
		this.setFocusable(true);
		this.canvas.drawBitmap(bitmap1,0,0,null);
		this.canvas.drawBitmap(bitmap2,lon,lat,null);
		return canvasBitmap;

	}

	

}
