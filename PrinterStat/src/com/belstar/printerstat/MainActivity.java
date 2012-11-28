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

import android.util.Log;
import android.view.View;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.SpinnerAdapter;
import android.widget.Toast;

public class MainActivity extends Activity {

	private Button mCommit = null;
	private EditText memoEdit;
	private StatSelView deviceNo = null;
	private StatSelView adminName;
	private StatSelView customName;
	private StatSelView archivesType = null;

	Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg) {
			if (msg.what == 1) {
				Bundle data = msg.getData();
				String xinghao = data.getString("xinghao");
				String num = data.getString("num");
				String xmldata = "<data><xinghao>" + xinghao
						+ "</xinghao><num>" + num + "</num></data>";
				mThread = new MyThread(xmldata);
				mThread.start();
			} else if (msg.what == 2) {
				new AlertDialog.Builder(MainActivity.this).setTitle("成功")
						.setMessage("数据发送成功").setPositiveButton("确定", null)
						.show();

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

		String data = this.getIntent().getStringExtra(Config.GET_DATA_KEY);

		final XmlGeter xmlGeter = new XmlGeter(data);

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

		deviceNo = (StatSelView) findViewById(R.id.deviceNo);
		deviceNo.setInitTvSelText(xmlGeter.getPrinterIDs());
		deviceNo.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				Toast.makeText(MainActivity.this, "dialog", Toast.LENGTH_LONG)
						.show();
				StatDialog dialog2 = new StatDialog(MainActivity.this,  R.style.Theme_dialog, xmlGeter.getPrinterIDs());
				dialog2.show();// 显示Dialog

			}
		});

		archivesType = (StatSelView) findViewById(R.id.archivesType);
		archivesType.setInitTvSelText(xmlGeter.getArchivesTypes());

		archivesType.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				Toast.makeText(MainActivity.this, "dialog", Toast.LENGTH_LONG)
						.show();
				// StatDialog dialog2 = new StatDialog(MainActivity.this, 180,
				// 180, R.layout.layout_dialog, R.style.Theme_dialog);
				// dialog2.show();//显示Dialog

			}
		});

		customName = (StatSelView) findViewById(R.id.customName);
		customName.setInitTvSelText(xmlGeter.getCustomNames());

		adminName = (StatSelView) findViewById(R.id.adminName);
		adminName.setInitTvSelText(xmlGeter.getAdminNames());

	}

}
