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
import org.apache.http.entity.ByteArrayEntity;
import org.apache.http.impl.client.DefaultHttpClient;

import com.belstar.printerstat.util.NetUtil;




import android.os.Bundle;
import android.os.Handler;
import android.os.Message;
import android.app.Activity;
import android.app.AlertDialog;
import android.text.InputType;
import android.view.View;
import android.view.View.OnClickListener;
import android.widget.ArrayAdapter;
import android.widget.Button;
import android.widget.EditText;
import android.widget.Spinner;
import android.widget.Toast;

public class MainActivity extends Activity {

	private Button mCommit = null;
	private EditText memoEdit;
	private Spinner deviceNo = null;
	private Spinner custName = null;
	private Spinner archivesType = null;
	

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
			String res = NetUtil.GetStringEntity(NetUtil.MakeRequest(post)); 
			if(res.equals("success")){
				Message msg = mHandler.obtainMessage();
				msg.what = 2;
				mHandler.sendMessage(msg);
			}
		};
	}
	
	MyThread mThread = null;

	
	

	
	


	
	@Override
	protected void onCreate(Bundle savedInstanceState) {
		super.onCreate(savedInstanceState);
		setContentView(R.layout.activity_main);

/*		mNum = (EditText) findViewById(R.id.num);
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
		});*/
		
		memoEdit = (EditText) findViewById(R.id.memo);
		deviceNo = (Spinner) findViewById(R.id.deviceNo);
		deviceNo.setAdapter(getDeviceNos());
		
		custName = (Spinner) findViewById(R.id.custName);
		custName.setAdapter(getCustNames());
		
		archivesType = (Spinner) findViewById(R.id.archivesType);
		archivesType.setAdapter(getArchivesTypes());
	}
	
	private ArrayAdapter<String> getDeviceNos(){
		List<String> list = new ArrayList<String>();
        list.add("BEIXING-GZ001");
        list.add("BEIXING-GZ002");
        list.add("BEIXING-GZ003"); 
        list.add("BEIXING-GZ006");
        list.add("BEIXING-GZ007");
        list.add("BEIXING-GZ009");
        list.add("BEIXING-GZ0016");
        list.add("BEIXING-GZ0017");
        list.add("BEIXING-GZ0019");
        list.add("BEIXING-GZ00216");
        list.add("BEIXING-GZ0027");
        list.add("BEIXING-GZ0029");
        list.add("BEIXING-GZ00316");
        list.add("BEIXING-GZ00416");
        list.add("BEIXING-GZ0037");
        list.add("BEIXING-GZ0039");
        list.add("BEIXING-GZ00616");
        list.add("BEIXING-GZ0067");
        list.add("BEIXING-GZ0069");
        list.add("BEIXING-GZ00816");
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.select_dialog_singlechoice,list);
        return adapter;
	}
	
	private ArrayAdapter<String> getCustNames(){
		List<String> list = new ArrayList<String>();
		list.add("刘一");
		list.add("陈二");
        list.add("张三");
        list.add("李四");
        list.add("王五"); 
        list.add("赵六");
        list.add("孙七");
        list.add("周八");
        list.add("吴九");
        list.add("郑十");

        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.select_dialog_singlechoice,list);
        return adapter;
	}
	
	private ArrayAdapter<String> getArchivesTypes(){
		List<String> list = new ArrayList<String>();
        list.add("图纸");
        list.add("图表");
        list.add("文字材料"); 
        ArrayAdapter<String> adapter = new ArrayAdapter<String>(this,android.R.layout.select_dialog_singlechoice,list);
        return adapter;
	}


}
