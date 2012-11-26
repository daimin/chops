package com.belstar.printerstat;


import org.apache.http.client.methods.HttpGet;
import org.apache.http.conn.ConnectTimeoutException;

import com.belstar.printerstat.util.NetUtil;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;

import android.content.Intent;


public class FirstActivity extends Activity {

	public static final int WHAT_INIT_THREAD  = 1;
	public static final int WHAT_XML_DATA  =  2;
	public static final int WHAT_NO_XML_DATA_TIMEOUT  =  3;
	public static final int WHAT_NO_XML_DATA_NO_CONN  =  4;
	
	class InitThread extends Thread{
		@Override
		public void run() {
			HttpGet get = new HttpGet(Config.GET_URL);

			
			String res = "";
			try {
				res = NetUtil.GetStringEntity(NetUtil.MakeRequest(get));
			} catch (ConnectTimeoutException e) {
				e.printStackTrace();
			} 
			if(res !=null && res.length() > 0){
				Message msg = mHandler.obtainMessage();
				Bundle data = new Bundle();
				data.putString(Config.GET_DATA_KEY, res);
				msg.setData(data);
				msg.what = WHAT_XML_DATA;
				mHandler.sendMessage(msg);
			}else{
				mHandler.sendEmptyMessage(WHAT_NO_XML_DATA_TIMEOUT);
			}
		}
	}
	
	InitThread mInitThread = null;

	
	
    Handler mHandler = new Handler(){
    	public void handleMessage(Message msg) {
    		if(msg.what == WHAT_INIT_THREAD){
    			mInitThread = new InitThread();
    			mInitThread.start();
    		}else if(msg.what == WHAT_XML_DATA){
    			Intent intent = new Intent(FirstActivity.this, MainActivity.class);
    			Bundle data = msg.getData();
    			intent.putExtra(Config.GET_DATA_KEY, data.getString(Config.GET_DATA_KEY));
    			startActivity(intent);
    			FirstActivity.this.finish();
    		}else if(msg.what == WHAT_NO_XML_DATA_TIMEOUT){
    			Intent intent = new Intent(FirstActivity.this, MainActivity.class);
    			startActivity(intent);
    			FirstActivity.this.finish();
    		}
    		
    	};
    };
	
	


	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_first);
        
		Message msg = mHandler.obtainMessage();
		msg.what = 1;
		mHandler.sendMessage(msg);
		


	}
	
	


}
