package com.belstar.printerstat;

import java.util.HashMap;
import java.util.List;
import java.util.Map;

import com.belstar.printerstat.entry.SelData;

import android.content.Context;
import android.graphics.drawable.Drawable;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
import android.view.MotionEvent;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;



public class StatSelView extends LinearLayout {

	private LayoutInflater mInflater = null;
	private View sel_item;
	private TextView tvTitle;
	private TextView tvSel;


	private ImageView ivIcon;
	private Drawable bg;
	
	private static Map<String, SelData> selViewData = null;


	
	public static Map<String, SelData> getSelViewData(Context ctx){
		if(selViewData == null){
			String hitAdmin = ctx.getResources().getString(R.string.hit_admin);
			String hitPrinterID = ctx.getResources().getString(R.string.hit_printer_ID);
			String hitArchivesType = ctx.getResources().getString(R.string.hit_archives_type);
			String hitCustom = ctx.getResources().getString(R.string.hit_custom);
			selViewData = new HashMap<String, SelData>();
			selViewData.put(hitAdmin, new SelData(hitAdmin,R.drawable.gongwenbao));
			selViewData.put(hitPrinterID, new SelData(hitAdmin,R.drawable.qianbi));
			selViewData.put(hitArchivesType, new SelData(hitAdmin,R.drawable.shuben));
			selViewData.put(hitCustom, new SelData(hitAdmin,R.drawable.maozi));
		}
		
		return selViewData;
	}

	public StatSelView(Context context, AttributeSet attrs) {
		super(context, attrs);
		
		String tagIvIcon = context.getResources().getString(R.string.tag_iv_icon);
		String tagTvSel = context.getResources().getString(R.string.tag_tv_sel);
		String tagIvTitle = context.getResources().getString(R.string.tag_tv_title);
		
		getSelViewData(context);
		
		mInflater = LayoutInflater.from(context);
		sel_item = mInflater.inflate(R.layout.sel_item, null);
		tvTitle = (TextView) sel_item.findViewWithTag(tagIvTitle);
		tvSel = (TextView) sel_item.findViewWithTag(tagTvSel);
		ivIcon = (ImageView) sel_item.findViewWithTag(tagIvIcon);
		
		String tag = this.getTag().toString();
		
		tvTitle.setText(tag);
		ivIcon.setImageResource(selViewData.get(tag).icon);
		

		this.addView(sel_item);
	}
	
	public TextView getTvSel() {
		return tvSel;
	}
	
	public void setInitTvSelText(List<String> selList){
		if(selList != null && selList.size() > 1){
			this.tvSel.setText(selList.get(0));
		}
	}

	
	@Override
	public boolean onTouchEvent(MotionEvent event) {
		int action = event.getAction();
		if(action == MotionEvent.ACTION_DOWN){
			bg = this.getBackground();
			this.setBackgroundDrawable(this.getResources().getDrawable(R.drawable.tyellow));
		}else if(action == MotionEvent.ACTION_UP){
			this.setBackgroundDrawable(bg);
			
		}
		
		return super.onTouchEvent(event);
		
	}

}
