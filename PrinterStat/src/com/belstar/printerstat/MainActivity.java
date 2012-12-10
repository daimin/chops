package com.belstar.printerstat;

import java.net.URLEncoder;
import java.util.Date;
import java.util.List;

import org.apache.http.client.methods.HttpPost;
import org.apache.http.conn.ConnectTimeoutException;
import org.apache.http.entity.ByteArrayEntity;


import com.belstar.printerstat.entry.SendData;
import com.belstar.printerstat.util.ComUtil;
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
import android.app.TimePickerDialog.OnTimeSetListener;
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

	public static final int FILE_WRITE_WHAT = 23;
	public static final int FILE_READ_WHAT = 24;

	public static final int UI_FILE_WRITE_WHAT = 35;
	public static final int UI_FILE_READ_WHAT = 36;

	public static final int SEND_WHAT = 11;
	public static final int SUCCESS_WHAT = 12;
	public static final int FAILURE_WHAT = 13;
	
	/**
	 * 返回值：成功
	 */
	public static final String RES_SUCCESS = "success";

	
	/**
	 * 日期和时间控件的ID
	 */
	private static final int DATE_DIALOG_ID = 0;
	private static final int TIME_DIALOG_ID = 1;
	
	public static final String XML_DATA_KEY = "xml_data";


	private StatSelView deviceNo = null;
	private StatSelView adminName;
	private StatSelView customName;
	private StatSelView archivesType = null;
	private StatSelView postTime = null;
	private StatSelView overTime = null;
	
	private EditText counterInitEdit;
	private EditText counterOverEdit;
	private EditText paperScrapEdit;
	private EditText archivesNumEdit;
	private EditText memoEdit;


	
	private Button saveBtn;
	private Button commitBtn;
	
	private StatSelView mTimeSelView = null;
	
	private DataThread mThread = null;

	Handler mHandler = new Handler() {

		@Override
		public void handleMessage(Message msg) {
			if (msg.what == SEND_WHAT) {
				Bundle data = msg.getData();
				String xmldata = data.getString(XML_DATA_KEY);
				mThread = new DataThread(xmldata);
				mThread.start(); 
			} else if (msg.what == SUCCESS_WHAT) {
				new AlertDialog.Builder(MainActivity.this)
				        .setTitle(MainActivity.this.getResources()
						.getString(R.string.dialog_success_title))
						.setIcon(android.R.drawable.ic_dialog_info)
						.setMessage(MainActivity.this.getResources().getString(R.string.dialog_success_cont))
						.setPositiveButton(MainActivity.this.getResources().getString(R.string.dialog_ok), null)
						.show();

			} else if(msg.what == FAILURE_WHAT){
				new AlertDialog.Builder(MainActivity.this)
		        .setTitle(MainActivity.this.getResources()
				.getString(R.string.dialog_failure_title))
				.setIcon(android.R.drawable.ic_dialog_alert)
				.setMessage(MainActivity.this.getResources().getString(R.string.dialog_failure_cont))
				.setPositiveButton(MainActivity.this.getResources().getString(R.string.dialog_ok), null)
				.show();
			}else if (msg.what == FILE_WRITE_WHAT) {
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
            this.xmldata = URLEncoder.encode(this.xmldata);
			ByteArrayEntity contents = new ByteArrayEntity(
					this.xmldata.getBytes());
			post.setEntity(contents);
			String res = "";
			try {
				res = NetUtil.GetStringEntity(NetUtil.MakeRequest(post));
				
			} catch (ConnectTimeoutException e) {
				e.printStackTrace();
				
			}
			if (res != null && res.equals(RES_SUCCESS)) {
				Message msg = mHandler.obtainMessage();
				msg.what = SUCCESS_WHAT;
				mHandler.sendMessage(msg);
			}else{
				Message msg = mHandler.obtainMessage();
				msg.what = FAILURE_WHAT;
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
		postTime.setTvSelText(ComUtil.getTime());
		postTime.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				mTimeSelView = ssv;
				showDialog(TIME_DIALOG_ID);
			}
		});
		overTime = (StatSelView)findViewById(R.id.overTime);
		overTime.setTvSelText(ComUtil.getTime());
		overTime.setOnClickListener(new View.OnClickListener() {
			
			@Override
			public void onClick(View v) {
				final StatSelView ssv = (StatSelView) v;
				mTimeSelView = ssv;
				showDialog(TIME_DIALOG_ID);
			}
		});

		memoEdit = (EditText) findViewById(R.id.memo);
		counterInitEdit = (EditText) findViewById(R.id.counterInit);
		counterOverEdit = (EditText) findViewById(R.id.counterOver);
		archivesNumEdit = (EditText) findViewById(R.id.archivesNum);
		paperScrapEdit = (EditText) findViewById(R.id.paperScrap);
		saveBtn = (Button) findViewById(R.id.saveBtn);
		commitBtn = (Button) findViewById(R.id.commitBtn);
		commitBtn.setOnClickListener(new Button.OnClickListener(){

			@Override
			public void onClick(View arg0) {
				
				String xmlData = MainActivity.this.getPustData();
				Message msg = mHandler.obtainMessage();
				Bundle data = new Bundle();
				msg.what = SEND_WHAT;
				data.putString(XML_DATA_KEY, xmlData);
				msg.setData(data);
				mHandler.sendMessage(msg);
			}
			
		});
	}
	
	private String getPustData(){
		SendData sendData = new SendData();
		sendData.setAdminName(adminName.getTvSel().getText().toString());
		int archivesNum = 0;
		try{
			archivesNum = Integer.parseInt(archivesNumEdit.getText().toString().trim());
		}catch(NumberFormatException nfe){
			archivesNum = 0;
		}
		
		sendData.setArchivesNum(archivesNum);
		sendData.setArchivesType(archivesType.getTvSel().getText().toString());
		int countInit = 0;
		try{
			countInit = Integer.parseInt(counterInitEdit.getText().toString().trim());
		}catch(NumberFormatException nfe){
			countInit = 0;
		}
		
		sendData.setCounterInit(countInit);
		int countOver = 0;
		try{
			countOver = Integer.parseInt(counterOverEdit.getText().toString().trim());
		}catch(NumberFormatException nfe){
			countOver = 0;
		}
		sendData.setCounterOver(countOver);
		sendData.setCustomName(customName.getTvSel().getText().toString());
		sendData.setMemo(memoEdit.getText().toString());
		sendData.setPostTime(postTime.getTvSel().getText().toString());
		sendData.setOverTime(overTime.getTvSel().getText().toString());
		int paperScrap = 0;
		try{
			paperScrap = Integer.parseInt(paperScrapEdit.getText().toString().trim());
		}catch(NumberFormatException nfe){
			paperScrap = 0;
		}
		sendData.setPaperScrap(paperScrap);
		sendData.setPrinterID(deviceNo.getTvSel().getText().toString());
		sendData.setSendTime(ComUtil.getDateTime());
		
		
		return XmlGeter.getSendDataXml(sendData);
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
		switch(id){
		case DATE_DIALOG_ID:
		case TIME_DIALOG_ID:
			String curTime = mTimeSelView.getTvSel().getText().toString();
			final Date curDate = ComUtil.parseTime(curTime);
			return new TimePickerDialog(MainActivity.this, new OnTimeSetListener() {

				@Override
				public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
				
					mTimeSelView.setTvSelText(ComUtil.getTimeByHourMin(hourOfDay, minute));

				}
			}, curDate.getHours(), curDate.getMinutes(), true);
		}
		return super.onCreateDialog(id, args);
	}
	
	@Override
	protected void onPrepareDialog(int id, Dialog dialog, Bundle args) {
		// TODO Auto-generated method stub
		super.onPrepareDialog(id, dialog, args);
	}

}
