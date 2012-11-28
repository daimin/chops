package com.belstar.printerstat;

import java.util.List;

import android.app.Activity;
import android.app.AlertDialog;

import android.content.Context;
import android.content.res.Resources;
import android.util.DisplayMetrics;
import android.view.Gravity;
import android.view.View;
import android.view.Window;
import android.view.WindowManager.LayoutParams;
import android.widget.TextView;

public class StatDialog extends AlertDialog {

	private Context ctx = null;
	private DisplayMetrics dm;  
	private TextView dialogTitle = null;
	private String title = null;
	
	public StatDialog(Context context, int style,List<String> listdata, String title) {
		super(context, style);
		this.ctx = context;
		this.title = title;
	}
	
	private void setLayout(){
		setContentView(R.layout.layout_dialog);

		Window win = this.getWindow();
		LayoutParams params = new LayoutParams();
		
		dm = new DisplayMetrics();   
        ((Activity)ctx).getWindowManager().getDefaultDisplay().getMetrics(dm);
        

		params.width = (int) ( dm.widthPixels  * 0.8);
		params.height = LayoutParams.WRAP_CONTENT;
		
		params.gravity = Gravity.TOP;
		win.setAttributes(params);
		this.setCanceledOnTouchOutside(true);// 设置点击Dialog外部任意区域关闭Dialog
		dialogTitle = (TextView) this.findViewById(R.id.dialog_title);
		dialogTitle.setText(this.title);
	}

	private float getDensity(Context context) {
		Resources resources = context.getResources();
		DisplayMetrics dm = resources.getDisplayMetrics();
		return dm.density;
	}
	
	@Override
	public void show() {
		
		super.show();
		setLayout();
	}

}