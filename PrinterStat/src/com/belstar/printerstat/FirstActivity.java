package com.belstar.printerstat;


import org.apache.http.client.methods.HttpGet;

import com.belstar.printerstat.util.NetUtil;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;

import android.content.Intent;


public class FirstActivity extends Activity {

	
	class InitThread extends Thread{
		@Override
		public void run() {
			HttpGet get = new HttpGet(Config.GET_URL);

			
			String res = NetUtil.GetStringEntity(NetUtil.MakeRequest(get)); 
			if(res !=null && res.length() > 0){
				Message msg = mHandler.obtainMessage();
				Bundle data = new Bundle();
				data.putString(Config.GET_DATA_KEY, res);
				msg.setData(data);
				msg.what = 2;
				mHandler.sendMessage(msg);
			}
		}
	}
	
	InitThread mInitThread = null;

	
	
    Handler mHandler = new Handler(){
    	public void handleMessage(Message msg) {
    		if(msg.what == 1){
    			mInitThread = new InitThread();
    			mInitThread.start();
    		}else if(msg.what == 2){
    			Intent intent = new Intent(FirstActivity.this, MainActivity.class);
    			Bundle data = msg.getData();
    			intent.putExtra(Config.GET_DATA_KEY, data.getString(Config.GET_DATA_KEY));
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
