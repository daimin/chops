package com.belstar.printerstat;

import java.util.List;

import android.app.AlertDialog;

import android.content.Context;
import android.content.res.Resources;
import android.util.DisplayMetrics;
import android.view.Gravity;
import android.view.Window;
import android.view.WindowManager.LayoutParams;

public class StatDialog extends AlertDialog {

	Context ctx = null;
	public StatDialog(Context context, int style,List<String> listdata) {
		super(context, style);
		this.ctx = context;
	}
	
	private void setLayout(){
		setContentView(R.layout.layout_dialog);

		Window win = this.getWindow();
		LayoutParams params = new LayoutParams();
		

		float density = getDensity(this.ctx);
		params.width = (int) (320 * density);
		params.height = (int) (480 * density);
		params.gravity = Gravity.CENTER;
		win.setAttributes(params);
		this.setCanceledOnTouchOutside(true);// 设置点击Dialog外部任意区域关闭Dialog
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