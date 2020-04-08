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

import android.os.ConditionVariable;
import android.provider.MediaStore;
import android.view.View;
import android.view.Menu;
import android.view.MenuItem;
import android.widget.ImageView;
import android.widget.TextView;
import android.widget.Toast;

import java.time.LocalDateTime;

import static android.view.View.GONE;

public class MainActivity extends AppCompatActivity {
    private TextView infoField;
    private TextView startField;
    private ImageView imageView;
    private FloatingActionButton camera;
    private FloatingActionButton info;
    private FloatingActionButton upload;
    private int animationDuration;
    private PackageManager packageManager;
    private Uri imageUri;

    private boolean showInfo = false;
    static final int REQUEST_IMAGE_CAPTURE = 1;
    static final int PERMISSIONS_REQUEST_CAMERA = 2;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        packageManager = getPackageManager();

        infoField = findViewById(R.id.infoView);
        startField = findViewById(R.id.textView);
        imageView = findViewById(R.id.image);

        animationDuration = getResources().getInteger(
                android.R.integer.config_longAnimTime);

        camera = findViewById(R.id.camera);
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
            showImage();
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

    private void showImage() {
        infoField.setVisibility(GONE);
        startField.setVisibility(GONE);
        showInfo = false;
        imageView.setImageURI(imageUri);
        imageView.setVisibility(View.VISIBLE);
    }

    private void showInfo() {
        imageView.setVisibility(GONE);
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
                        startField.setVisibility(GONE);
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
                        infoField.setVisibility(GONE);
                    }
                });
        showInfo = false;
    }
    
}
