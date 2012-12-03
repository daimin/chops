package com.belstar.printerstat;

import java.util.List;

import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ConnectTimeoutException;
import org.apache.http.entity.ByteArrayEntity;


import com.belstar.printerstat.util.FileOperator;
import com.belstar.printerstat.util.NetUtil;
import com.belstar.printerstat.util.XmlGeter;

import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;
import android.app.AlertDialog;
import android.app.Dialog;
import android.app.TimePickerDialog;
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
import android.widget.TimePicker;
import android.widget.Toast;

public class MainActivity extends Activity {

	public static final int FILE_WRITE_WHAT = 3;
	public static final int FILE_READ_WHAT = 4;

	public static final int UI_FILE_WRITE_WHAT = 5;
	public static final int UI_FILE_READ_WHAT = 6;

	public static final int SEND_WHAT = 1;
	public static final int SUCCESS_WHAT = 2;
	
	public static final String XML_DATA_KEY = "xml_data";

	private Button mCommitBtn = null;
	private EditText memoEdit;
	private StatSelView deviceNo = null;
	private StatSelView adminName;
	private StatSelView customName;
	private StatSelView archivesType = null;
	private StatSelView postTime = null;
	private StatSelView overTime = null;
	
	private EditText counterInitEdit;
	private EditText counterOverEdit;
	private EditText paperScrapEdit;
	private Button saveBtn;
	
	private DataThread mThread = null;

	Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg) {
			if (msg.what == SEND_WHAT) {
				Bundle data = msg.getData();
				String xinghao = data.getString("xinghao");
				String num = data.getString("num");
				String xmldata = "<data><xinghao>" 
				        + xinghao
						+ "</xinghao><num>" 
				        + num 
				        + "</num></data>";
				mThread = new DataThread(xmldata);
				mThread.start();
			} else if (msg.what == SUCCESS_WHAT) {
				new AlertDialog.Builder(MainActivity.this).setTitle("成功")
						.setMessage("数据发送成功").setPositiveButton("确定", null)
						.show();

			} else if (msg.what == FILE_WRITE_WHAT) {
				Bundle data = msg.getData();
				String xmlData = data.getString(Config.GET_DATA_KEY);
				FileOperator.writeXMlDataFile(MainActivity.this, xmlData);
			}
		}

	};


	class DataThread extends Thread {
		String xmldata = "";

		public DataThread(String xmldata) {
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
				Log.i("MainActivity", res);
			} catch (ConnectTimeoutException e) {
				e.printStackTrace();
			}
			if (res.equals("success")) {
				Message msg = mHandler.obtainMessage();
				msg.what = 2;
				mHandler.sendMessage(msg);
			}
		};
	}



	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

		boolean getFromNet = false;
		String data = this.getIntent().getStringExtra(Config.GET_DATA_KEY);
		if (data == null || data.length() <= 0) {
			data = this.getIntent().getStringExtra(Config.TIMEOUT_KEY);
		} else {
			getFromNet = true;
		}
		if (getFromNet == false) {

			if (data != null && data.length() > 0) {
				// TIMEOUT后得到的数据
				Toast.makeText(this,
						this.getResources().getString(R.string.time_out_val),
						Toast.LENGTH_LONG).show();
			} else {
				// 无法连接后得到的数据
				data = this.getIntent().getStringExtra(Config.NO_NET_CONN_KEY);
				if (data != null && data.length() > 0) {
					Toast.makeText(
							this,
							this.getResources().getString(R.string.no_conn_val),
							Toast.LENGTH_LONG).show();
				}
			}

		}

		initSelView(data);
		if (getFromNet) {
			Message msg = mHandler.obtainMessage();
			Bundle bundle = new Bundle();
			bundle.putString(Config.GET_DATA_KEY, data);
			msg.setData(bundle);
			msg.what = FILE_WRITE_WHAT;
			mHandler.sendMessage(msg);
		}

		mCommitBtn = (Button) findViewById(R.id.commitBtn);

		mCommitBtn.setOnClickListener(new Button.OnClickListener() {

			@Override
			public void onClick(View v) {
				
					Message msg = mHandler.obtainMessage();
					msg.what = 1;
					Bundle data = new Bundle();
					data.putString("xinghao", "dsdsdssd");
					data.putString("num", "122");
					msg.setData(data);
					mHandler.sendMessage(msg);
			}
		});

		memoEdit = (EditText) findViewById(R.id.memo);

	}

	private void initSelView(String txtData) {
		final XmlGeter xmlGeter = new XmlGeter(txtData);

		deviceNo = (StatSelView) findViewById(R.id.deviceNo);
		deviceNo.setInitTvSelText(xmlGeter.getPrinterIDs());
		deviceNo.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(final View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrPrinterIdArr = toArray(xmlGeter
						.getPrinterIDs());
				StatDialog.getDialog(MainActivity.this,
						R.string.hit_printer_ID, ssv, arrPrinterIdArr).show();

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
				StatDialog.getDialog(MainActivity.this,
						R.string.hit_archives_type, ssv, arrArchivesTypes)
						.show();

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
				StatDialog.getDialog(MainActivity.this, R.string.hit_custom,
						ssv, arrCustomNames).show();

			}
		});

		adminName = (StatSelView) findViewById(R.id.adminName);
		adminName.setInitTvSelText(xmlGeter.getAdminNames());
		adminName.setOnClickListener(new View.OnClickListener() {

			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				final String[] arrAdminNames = toArray(xmlGeter.getAdminNames());
				StatDialog.getDialog(MainActivity.this, R.string.hit_admin,
						ssv, arrAdminNames).show();

			}
		});
		
		postTime = (StatSelView)findViewById(R.id.postTime);
		postTime.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				StatDialog.getTimePickerDialog(MainActivity.this, ssv);
				Bundle args = new Bundle();
			}
		});
		overTime = (StatSelView)findViewById(R.id.overTime);
		
		memoEdit = (EditText) findViewById(R.id.memo);
		counterInitEdit = (EditText) findViewById(R.id.counterInit);
		counterOverEdit = (EditText) findViewById(R.id.counterOver);
		paperScrapEdit = (EditText) findViewById(R.id.paperScrap);
		saveBtn = (Button) findViewById(R.id.saveBtn);
	}
	
	private String getPustData(){
		StringBuffer xmlBuf = new StringBuffer();
		
		return "";
	}

	private String[] toArray(List<String> strList) {
		if (strList == null) {
			return new String[] {};
		}
		int listLen = strList.size();
		String[] strArr = new String[listLen];
		for (int i = 0; i < listLen; i++) {
			strArr[i] = strList.get(i);
		}

		return strArr;
	}
	
	@Override
	protected Dialog onCreateDialog(int id, Bundle args) {
		// TODO Auto-generated method stub
		return super.onCreateDialog(id, args);
	}

}
