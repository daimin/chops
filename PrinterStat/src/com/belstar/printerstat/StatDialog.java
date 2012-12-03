package com.belstar.printerstat;

import android.app.AlertDialog;
import android.app.DatePickerDialog;
import android.app.DatePickerDialog.OnDateSetListener;
import android.app.TimePickerDialog;
import android.app.TimePickerDialog.OnTimeSetListener;
import android.content.Context;
import android.content.DialogInterface;
import android.widget.DatePicker;
import android.widget.TimePicker;

public class StatDialog {

	public static AlertDialog getDialog(Context ctx, int hit_res,
			final StatSelView ssv, final String[] dataArr) {
		AlertDialog dlg = new AlertDialog.Builder(ctx)
				.setTitle(ctx.getResources().getString(hit_res))
				.setIcon(android.R.drawable.ic_menu_more)
				.setNeutralButton("取消", new DialogInterface.OnClickListener() {

					@Override
					public void onClick(DialogInterface dialog, int which) {
						dialog.dismiss();

					}

				})
				.setSingleChoiceItems(dataArr, ssv.getChckItem(),
						new DialogInterface.OnClickListener() {
							@Override
							public void onClick(DialogInterface dialog,
									int which) {

								ssv.setChckItem(which);
								ssv.setTvSelText(dataArr[which]);

								dialog.dismiss();

							}
						}).create();

		return dlg;

	}

	public static TimePickerDialog getTimePickerDialog(Context ctx,
			final StatSelView ssv) {
		return new TimePickerDialog(ctx, new OnTimeSetListener() {

			@Override
			public void onTimeSet(TimePicker view, int hourOfDay, int minute) {
				ssv.setTvSelText(hourOfDay + ":" + minute);

			}
		}, 23, 25, true);
	}

	public static void alertDialog(Context ctx, String title, String content) {
		new AlertDialog.Builder(ctx)
				.setTitle(title)
				.setIcon(
						ctx.getResources().getDrawable(
								android.R.drawable.ic_dialog_alert))
				.setMessage(content)
				.setPositiveButton(
						ctx.getResources().getString(R.string.dialog_ok), null)
				.show();
	}
}
