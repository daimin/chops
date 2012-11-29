package com.belstar.printerstat;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.util.List;

import org.apache.http.HttpEntity;
import org.apache.http.HttpResponse;
import org.apache.http.client.ClientProtocolException;
import org.apache.http.client.methods.HttpPost;
import org.apache.http.client.methods.HttpUriRequest;
import org.apache.http.conn.ConnectTimeoutException;
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import com.belstar.printerstat.util.NetUtil;
import com.belstar.printerstat.util.XmlGeter;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;

import android.util.DisplayMetrics;
import android.util.Log;
import android.view.Gravity;
import android.view.LayoutInflater;
import android.view.View;
import android.view.Window;
import android.view.WindowManager.LayoutParams;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;
import android.widget.TextView;
import android.widget.Toast;

public class MainActivity extends Activity {

	public static final int FILE_WRITE_WHAT = 3;
	public static final int SEND_WHAT = 1;
	public static final int SUCCESS_WHAT = 2;
	
	private Button mCommit = null;
	private EditText memoEdit;
	private StatSelView deviceNo = null;
	private StatSelView adminName;
	private StatSelView customName;
	private StatSelView archivesType = null;

	Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg) {
			if (msg.what == SEND_WHAT) {
				Bundle data = msg.getData();
				String xinghao = data.getString("xinghao");
				String num = data.getString("num");
				String xmldata = "<data><xinghao>" + xinghao
						+ "</xinghao><num>" + num + "</num></data>";
				mThread = new MyThread(xmldata);
				mThread.start();
			} else if (msg.what == SUCCESS_WHAT) {
				new AlertDialog.Builder(MainActivity.this).setTitle("成功")
						.setMessage("数据发送成功").setPositiveButton("确定", null)
						.show();

			}else if(msg.what == FILE_WHAT){
				
			}
		}

	};

	class MyThread extends Thread {
		String xmldata = "";

		public MyThread(String xmldata) {
			this.xmldata = xmldata;
		}

		public void run() {
			HttpPost post = new HttpPost(Config.PUT_URL);

			ByteArrayEntity contents = new ByteArrayEntity(
					this.xmldata.getBytes());
			post.setEntity(contents);
			String res = null;
			try {
				res = NetUtil.GetStringEntity(NetUtil.MakeRequest(post));
			} catch (ConnectTimeoutException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
			if (res.equals("success")) {
				Message msg = mHandler.obtainMessage();
				msg.what = 2;
				mHandler.sendMessage(msg);
			}
		};
	}

	MyThread mThread = null;

	InitThread mInitThread = null;

	class InitThread extends Thread {
		@Override
		public void run() {

		}
	}
	
	

	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		boolean getFromNet = false;
		String data = this.getIntent().getStringExtra(Config.GET_DATA_KEY);
		if(data == null || data.length() <= 0){
			data = this.getIntent().getStringExtra(Config.TIMEOUT_KEY);
			getFromNet = true;

		}
		if(data != null && data.length() > 0){
			Toast.makeText(this, data, Toast.LENGTH_LONG).show();
		}else{
			data = this.getIntent().getStringExtra(Config.NO_NET_CONN_KEY);
		}
		
		if(data != null && data.length() > 0){
			Toast.makeText(this, data, Toast.LENGTH_LONG).show();
		}
		
		if(getFromNet){
			initSelView(data);
			Message msg = mHandler.obtainMessage();
			msg.what = FILE_WRITE_WHAT;
			mHandler.sendEmptyMessage(FILE_WRITE_WHAT);
		}else{
			Message msg = mHandler.obtainMessage();
			msg.what = FILE_WRITE_WHAT;
			mHandler.sendEmptyMessage(FILE_WRITE_WHAT);
		}
		


		/*
		 * mNum = (EditText) findViewById(R.id.num); mXinghao = (EditText)
		 * findViewById(R.id.xinghao); mCommit = (Button)
		 * findViewById(R.id.commit);
		 * 
		 * mCommit.setOnClickListener(new OnClickListener() {
		 * 
		 * @Override public void onClick(View v) { String numVal =
		 * mNum.getText().toString().trim(); String xinghaoVal =
		 * mXinghao.getText().toString().trim(); if(!isNull(numVal) &&
		 * !isNull(xinghaoVal)){ Message msg = mHandler.obtainMessage();
		 * msg.what = 1; Bundle data = new Bundle(); data.putString("xinghao",
		 * xinghaoVal); data.putString("num", numVal); msg.setData(data);
		 * mHandler.sendMessage(msg); }else{ Toast.makeText(MainActivity.this,
		 * "型号和纸张数不能为空", Toast.LENGTH_SHORT).show(); } } });
		 */

		memoEdit = (EditText) findViewById(R.id.memo);

		

	}
	


	private void initSelView(String txtData){
		final XmlGeter xmlGeter = new XmlGeter(txtData);

		deviceNo = (StatSelView) findViewById(R.id.deviceNo);
		deviceNo.setInitTvSelText(xmlGeter.getPrinterIDs());
		deviceNo.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(final View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrPrinterIdArr = toArray(xmlGeter
						.getPrinterIDs());
				StatDialog.getDialog(MainActivity.this, R.string.hit_printer_ID, ssv, arrPrinterIdArr).show();

			}
		});

		archivesType = (StatSelView) findViewById(R.id.archivesType);
		archivesType.setInitTvSelText(xmlGeter.getArchivesTypes());

		archivesType.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrArchivesTypes = toArray(xmlGeter
						.getArchivesTypes());
				StatDialog.getDialog(MainActivity.this, R.string.hit_archives_type, ssv, arrArchivesTypes).show();

			}
		});

		customName = (StatSelView) findViewById(R.id.customName);
		customName.setInitTvSelText(xmlGeter.getCustomNames());
		customName.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrCustomNames = toArray(xmlGeter
						.getCustomNames());
				StatDialog.getDialog(MainActivity.this, R.string.hit_custom, ssv, arrCustomNames).show();
				
			}
		});

		adminName = (StatSelView) findViewById(R.id.adminName);
		adminName.setInitTvSelText(xmlGeter.getAdminNames());
		adminName.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrAdminNames = toArray(xmlGeter
						.getAdminNames());
				StatDialog.getDialog(MainActivity.this, R.string.hit_admin, ssv, arrAdminNames).show();
				
			}
		});
	}
	
	private String[] toArray(List<String> strList) {
		int listLen = strList.size();
		String[] strArr = new String[listLen];
		for (int i = 0; i < listLen; i++) {
			strArr[i] = strList.get(i);
		}

		return strArr;
	}

}
