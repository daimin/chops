package com.belstar.printerstat;

import android.content.Context;
import android.util.AttributeSet;
import android.util.Log;
import android.view.LayoutInflater;
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

	public StatSelView(Context context, AttributeSet attrs) {
		super(context, attrs);
		mInflater = LayoutInflater.from(context);
		sel_item = mInflater.inflate(R.layout.sel_item, null);
		tvTitle = (TextView) sel_item.findViewWithTag("tv_title");
		tvSel = (TextView) sel_item.findViewWithTag("tv_sel");
		ivIcon = (ImageView) sel_item.findViewWithTag("iv_icon");
		String tag = this.getTag().toString();
		String []tags = tag.split("|");
		tvTitle.setText(tags[0]);
		tvTitle.setText(tags[0]);

		this.addView(sel_item);
	}

}
