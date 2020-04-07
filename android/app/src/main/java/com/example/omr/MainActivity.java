package com.example.omr;

import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;

import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.TextView;

public class MainActivity extends AppCompatActivity {
    private TextView infoField;
    private TextView startField;
    private FloatingActionButton camera;
    private FloatingActionButton info;
    private FloatingActionButton upload;
    private int animationDuration;

    private boolean showInfo = false;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        infoField = findViewById(R.id.infoView);
        startField = findViewById(R.id.textView);

        animationDuration = getResources().getInteger(
                android.R.integer.config_longAnimTime);

        camera = findViewById(R.id.camera);
        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });

        info = findViewById(R.id.info);
        info.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (!showInfo) {
                    showInfo();
                } else {
                    hideInfo();
                }
            }
        });

        upload = findViewById(R.id.upload);
        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }

    private void showInfo() {
        infoField.setAlpha(0f);
        infoField.setVisibility(View.VISIBLE);
        infoField.animate()
                .alpha(1f)
                .setDuration(animationDuration)
                .setListener(null);
        startField.animate()
                .alpha(0f)
                .setDuration(animationDuration)
                .setListener(new AnimatorListenerAdapter() {
                    @Override
                    public void onAnimationEnd(Animator animation) {
                        startField.setVisibility(View.GONE);
                    }
                });
        showInfo = true;
    }

    private void hideInfo() {
        startField.setAlpha(0f);
        startField.setVisibility(View.VISIBLE);
        startField.animate()
                .alpha(1f)
                .setDuration(animationDuration)
                .setListener(null);
        infoField.animate()
                .alpha(0f)
                .setDuration(animationDuration)
                .setListener(new AnimatorListenerAdapter() {
                    @Override
                    public void onAnimationEnd(Animator animation) {
                        infoField.setVisibility(View.GONE);
                    }
                });
        showInfo = false;
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        // Inflate the menu; this adds items to the action bar if it is present.
        getMenuInflater().inflate(R.menu.menu_main, menu);
        return true;
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        // Handle action bar item clicks here. The action bar will
        // automatically handle clicks on the Home/Up button, so long
        // as you specify a parent activity in AndroidManifest.xml.
        int id = item.getItemId();

        //noinspection SimplifiableIfStatement
        if (id == R.id.action_settings) {
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
