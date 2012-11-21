package com.belstar.printerstat;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import cn.vaga.printerstat.R;



import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;
import android.app.AlertDialog;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Toast;

public class MainActivity extends Activity {

	private EditText mNum = null;
	private EditText mXinghao = null;
	private Button mCommit = null;

	Handler mHandler = new Handler(){

		@Override
		public void handleMessage(Message msg) {
			if(msg.what == 1){
				Bundle data = msg.getData();
				String xinghao = data.getString("xinghao");
				String num = data.getString("num");
				String xmldata = "<data><xinghao>"+xinghao+"</xinghao><num>"+num+"</num></data>";
				mThread = new MyThread(xmldata);
				mThread.start();
			}else if(msg.what == 2){
				new AlertDialog.Builder(MainActivity.this)
				               .setTitle("成功")
				               .setMessage("数据发送成功")
				               .setPositiveButton("确定", null)
				               .show();
				                
			}
		}
		
		
	};
	
	class MyThread extends Thread{
		String xmldata = "";
		public MyThread(String xmldata){
			this.xmldata = xmldata;
		}
		
		public void run() {
			HttpPost post = new HttpPost(Config.URL);

			ByteArrayEntity contents = new ByteArrayEntity(this.xmldata.getBytes());
			post.setEntity(contents);
			String res = MainActivity.this.GetStringEntity(MakeRequest(post));
			if(res.equals("success")){
				Message msg = mHandler.obtainMessage();
				msg.what = 2;
				mHandler.sendMessage(msg);
			}
		};
	}
	
	MyThread mThread = null;

	/**
	 * 得到服务器响应的返回的字符串
	 * 
	 * @param response
	 * @return
	 */
	private String GetStringEntity(HttpResponse response) {
		if (response == null) {
			return null;
		}
		HttpEntity entity = response.getEntity();
		if (entity != null)
			try {
				return StreamToString(entity.getContent());
			} catch (IllegalStateException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		return null;
	}
	
	/**
	 * 读取输入流中传入的字符串
	 * 
	 * @param is
	 * @return 字符串，如果读取失败返回null
	 */
	private static String StreamToString(InputStream is) {
		BufferedReader reader = new BufferedReader(new InputStreamReader(is));
		String ret = "";
		String line;
		try {
			while ((line = reader.readLine()) != null) {
				ret += line;
			}
			return ret;
		} catch (IOException e) {
			e.printStackTrace();
		}
		return null;
	}
	
	
	private static HttpResponse MakeRequest(HttpUriRequest areq) {
		DefaultHttpClient HttpManager = new DefaultHttpClient();
		try {
			final HttpResponse response = HttpManager.execute(areq);
			return response;
		} catch (ClientProtocolException e) {
			e.printStackTrace();
		} catch (IOException e) {

			e.printStackTrace();
		}
		return null;

	}
	
	/**
	 * 得到服务器响应的返回的输入流
	 * 
	 * @param response
	 * @return
	 */
	private static InputStream GetInputStreamEntity(HttpResponse response) {
		if (response == null) {
			return null;
		}
		HttpEntity entity = response.getEntity();
		if (entity != null)
			try {
				return entity.getContent();
			} catch (IllegalStateException e) {
				e.printStackTrace();
			} catch (IOException e) {
				e.printStackTrace();
			}
		return null;
	}
	

	
	
	private boolean isNull(String txt){
		if(null == txt || txt.trim().equals("")){
			return true;
		}
		return false;
	}

	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		mNum = (EditText) findViewById(R.id.num);
		mXinghao = (EditText) findViewById(R.id.xinghao);
		mCommit = (Button) findViewById(R.id.commit);

		mCommit.setOnClickListener(new OnClickListener() {

			@Override
			public void onClick(View v) {
				String numVal = mNum.getText().toString().trim();
				String xinghaoVal = mXinghao.getText().toString().trim();
				if(!isNull(numVal) && !isNull(xinghaoVal)){
					Message msg = mHandler.obtainMessage(); 
					msg.what = 1;
					Bundle data = new Bundle();
					data.putString("xinghao", xinghaoVal);
					data.putString("num", numVal);
					msg.setData(data);
					mHandler.sendMessage(msg);
				}else{
					Toast.makeText(MainActivity.this, "型号和纸张数不能为空", Toast.LENGTH_SHORT).show();
				}
			}
		});
	}


}
