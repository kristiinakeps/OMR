package com.example.omr;

import android.Manifest;
import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.graphics.Bitmap;
import android.net.Uri;
import android.os.Bundle;

import com.google.android.material.floatingactionbutton.FloatingActionButton;
import com.google.android.material.snackbar.Snackbar;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import android.os.ConditionVariable;
import android.provider.MediaStore;
import android.text.Layout;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import java.time.LocalDateTime;

import static android.view.View.GONE;

public class MainActivity extends AppCompatActivity {
    private LinearLayout imageLayout;
    private ConstraintLayout infoLayout;
    private ConstraintLayout startLayout;
    private TextView infoField;
    private TextView startField;
    private ImageView imageView;
    private FloatingActionButton camera;
    private FloatingActionButton info;
    private FloatingActionButton upload;
    private FloatingActionButton play;
    private FloatingActionButton download;
    private int animationDuration;
    private PackageManager packageManager;
    private Uri imageUri;

    private boolean showStart = true;
    private boolean showImage = false;
    private boolean showInfo = false;

    static final int REQUEST_IMAGE_CAPTURE = 1;
    static final int PERMISSIONS_REQUEST_CAMERA = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        packageManager = getPackageManager();

        imageLayout = findViewById(R.id.imageLayout);
        infoLayout = findViewById(R.id.infoLayout);
        startLayout = findViewById(R.id.startLayout);

        infoField = findViewById(R.id.infoView);
        startField = findViewById(R.id.textView);
        imageView = findViewById(R.id.image);
        camera = findViewById(R.id.camera);
        info = findViewById(R.id.info);
        upload = findViewById(R.id.upload);


        animationDuration = getResources().getInteger(
                android.R.integer.config_longAnimTime);

        imageLayout.setVisibility(LinearLayout.GONE);
        infoLayout.setVisibility(ConstraintLayout.GONE);


        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)) {
                    if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED ||
                    checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED){
                        requestPermissions(new String[]{Manifest.permission.CAMERA, Manifest.permission.WRITE_EXTERNAL_STORAGE},
                                PERMISSIONS_REQUEST_CAMERA);
                    } else {
                        dispatchTakePictureIntent();
                    }
                }
            }
        });

        info.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                toggleInfo();
            }
        });

        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                Snackbar.make(view, "Replace with your own action", Snackbar.LENGTH_LONG)
                        .setAction("Action", null).show();
            }
        });
    }

    // https://developer.android.com/training/camera/photobasics
    private void dispatchTakePictureIntent() {
        ContentValues contentValues = new ContentValues();
        contentValues.put(MediaStore.Images.Media.TITLE, LocalDateTime.now().toString());
        imageUri = getContentResolver().insert(MediaStore.Images.Media.EXTERNAL_CONTENT_URI, contentValues);

        Intent takePictureIntent = new Intent(MediaStore.ACTION_IMAGE_CAPTURE);
        takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT, imageUri);
        if (takePictureIntent.resolveActivity(getPackageManager()) != null) {
            startActivityForResult(takePictureIntent, REQUEST_IMAGE_CAPTURE);
        }
    }

    // https://developer.android.com/training/camera/photobasics
    // https://www.youtube.com/watch?v=LpL9akTG4hI
    @Override
    protected void onActivityResult(int requestCode, int resultCode, Intent data) {
        if (requestCode == REQUEST_IMAGE_CAPTURE && resultCode == RESULT_OK) {
            imageView.setImageURI(imageUri);
            hideInfo();
            hideStart();
            showInfo = false;
            showStart = false;
            makeImageVisible();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        switch (requestCode) {
            case PERMISSIONS_REQUEST_CAMERA: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                        dispatchTakePictureIntent();
                } else {
                    Toast.makeText(this, "Rakendusel pole vajalikke ligipääse", Toast.LENGTH_LONG).show();
                }
                return;
            }
        }
    }


    private void toggleInfo() {
        if (showInfo) {
            hideInfo();
            if (showStart) makeStartVisible();
            else makeImageVisible();
        }
        else if (showStart) {
            makeInfoVisible();
            hideStart();
        } else {
            makeInfoVisible();
            hideImage();
        }
    }

    private void makeInfoVisible() {
        infoLayout.setVisibility(ConstraintLayout.VISIBLE);
        infoLayout.setAlpha(0f);
        infoLayout.animate()
                .alpha(1f)
                .setDuration(animationDuration)
                .setListener(null);
        showInfo = true;
    }

    private void makeStartVisible() {
        startLayout.setVisibility(ConstraintLayout.VISIBLE);
        startLayout.setAlpha(0f);
        startLayout.animate()
                .alpha(1f)
                .setDuration(animationDuration)
                .setListener(null);
        showStart = true;
    }

    private void makeImageVisible() {
        imageView.setVisibility(View.VISIBLE);
        imageLayout.setVisibility(LinearLayout.VISIBLE);
        imageLayout.setAlpha(0f);
        imageLayout.animate()
                .alpha(1f)
                .setDuration(animationDuration)
                .setListener(null);
        showImage = true;

    }

    private void hideInfo() {
        infoLayout.animate()
                .alpha(0f)
                .setDuration(animationDuration)
                .setListener(new AnimatorListenerAdapter() {
                    @Override
                    public void onAnimationEnd(Animator animation) {
                        infoLayout.setVisibility(ConstraintLayout.GONE);
                    }
                });
        showInfo = false;
    }

    private void hideStart() {
        startLayout.animate()
                .alpha(0f)
                .setDuration(animationDuration)
                .setListener(new AnimatorListenerAdapter() {
                    @Override
                    public void onAnimationEnd(Animator animation) {
                        startLayout.setVisibility(ConstraintLayout.GONE);
                    }
                });
    }

    private void hideImage() {
        imageLayout.animate()
                .alpha(0f)
                .setDuration(animationDuration)
                .setListener(new AnimatorListenerAdapter() {
                    @Override
                    public void onAnimationEnd(Animator animation) {
                        imageLayout.setVisibility(LinearLayout.GONE);
                    }
                });
    }


}
