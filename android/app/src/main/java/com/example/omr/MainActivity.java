package com.example.omr;

import android.Manifest;
import android.animation.Animator;
import android.animation.AnimatorListenerAdapter;
import android.content.ContentValues;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.net.Uri;
import android.os.Bundle;
import android.provider.MediaStore;
import android.view.View;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.TextView;
import android.widget.Toast;

import androidx.appcompat.app.AppCompatActivity;
import androidx.constraintlayout.widget.ConstraintLayout;

import com.android.volley.Request;
import com.android.volley.RequestQueue;
import com.android.volley.Response;
import com.android.volley.RetryPolicy;
import com.android.volley.VolleyError;
import com.android.volley.toolbox.JsonObjectRequest;
import com.android.volley.toolbox.StringRequest;
import com.android.volley.toolbox.Volley;
import com.google.android.material.floatingactionbutton.FloatingActionButton;

import org.json.JSONException;
import org.json.JSONObject;

import java.io.FileNotFoundException;
import java.io.InputStream;
import java.time.LocalDateTime;

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
    private FloatingActionButton recognize;
    private int animationDuration;
    private PackageManager packageManager;
    private Uri imageUri;

    private boolean showStart = true;
    private boolean showImage = false;
    private boolean showInfo = false;

    private final Recognitionservice recognitionservice = new Recognitionservice();
    RequestQueue queue;
    String url ="https://musicrecognition.herokuapp.com/";

    static final int REQUEST_IMAGE_CAPTURE = 1;
    static final int PERMISSIONS_REQUEST_CAMERA = 2;
    static final int PERMISSION_REQUEST_UPLOAD = 3;
    static final int REQUEST_IMAGE_UPLOAD = 4;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

         queue = Volley.newRequestQueue(this);

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
        recognize = findViewById(R.id.recognize);


        animationDuration = getResources().getInteger(
                android.R.integer.config_longAnimTime);

        imageLayout.setVisibility(LinearLayout.GONE);
        infoLayout.setVisibility(ConstraintLayout.GONE);


        camera.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (packageManager.hasSystemFeature(PackageManager.FEATURE_CAMERA_ANY)) {
                    if (checkSelfPermission(Manifest.permission.CAMERA) != PackageManager.PERMISSION_GRANTED ||
                            checkSelfPermission(Manifest.permission.WRITE_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
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
                info.setEnabled(false);
                toggleInfo();
            }
        });

        upload.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
                if (checkSelfPermission(Manifest.permission.READ_EXTERNAL_STORAGE) != PackageManager.PERMISSION_GRANTED) {
                    requestPermissions(new String[]{Manifest.permission.READ_EXTERNAL_STORAGE},
                            PERMISSION_REQUEST_UPLOAD);
                } else {
                    dispatchUploadPictureIntent();
                }
            }
        });
        recognize.setOnClickListener(new View.OnClickListener() {
            @Override
            public void onClick(View view) {
//                    StringRequest stringRequest = new StringRequest(Request.Method.POST, url,
//                            new Response.Listener<String>() {
//                                @Override
//                                public void onResponse(String response) {
//                                    System.out.println(response);
//                                }
//                            }, new Response.ErrorListener() {
//                        @Override
//                        public void onErrorResponse(VolleyError error) {
//                            System.out.println(error);
//                            Toast.makeText(getApplicationContext(), "Tekkis viga! Palun proovige uuesti.", Toast.LENGTH_LONG).show();
//                        }
//                    }) {
//                        @Override
//                        public byte[] getBody() {
//                            try {
//                                return recognitionservice.imageToBase64(getContentResolver().openInputStream(imageUri));
//                            } catch (Exception e) {
//                                e.printStackTrace();
//                                return null;
//                            }
//                        }
//                    };
//                    queue.add(stringRequest);
//            }
                try{
                    String base64 = recognitionservice.imageToBase64(getContentResolver().openInputStream(imageUri));
                    postData(base64);
                } catch (Exception e) {
                    e.printStackTrace();
                }
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
        } else if (requestCode == REQUEST_IMAGE_UPLOAD && resultCode == RESULT_OK && data != null) {
            Uri selectedImage =  data.getData();
            imageUri = selectedImage;
            imageView.setImageURI(imageUri);
            hideInfo();
            hideStart();
            showInfo = false;
            showStart = false;
            makeImageVisible();
        }
    }

    private void dispatchUploadPictureIntent() {
        Intent pickPhoto = new Intent(Intent.ACTION_PICK, android.provider.MediaStore.Images.Media.EXTERNAL_CONTENT_URI);
        startActivityForResult(pickPhoto, REQUEST_IMAGE_UPLOAD);
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
                break;
            }
            case PERMISSION_REQUEST_UPLOAD: {
                if (grantResults.length > 0
                        && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    dispatchUploadPictureIntent();
                } else {
                    Toast.makeText(this, "Rakendusel pole vajalikke ligipääse", Toast.LENGTH_LONG).show();
                }
            }
        }
    }


    private void toggleInfo() {
        if (showInfo) {
            hideInfo();
            if (showStart) makeStartVisible();
            else makeImageVisible();
        } else if (showStart) {
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
                        info.setEnabled(true);
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
                        info.setEnabled(true);
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
                        info.setEnabled(true);
                    }
                });
    }

    // Post Request For JSONObject
    public void postData(String base64) {
        RequestQueue requestQueue = Volley.newRequestQueue(getApplicationContext());
        JSONObject object = new JSONObject();
        try {
            object.put("image",base64);
        } catch (JSONException e) {
            e.printStackTrace();
        }
        JsonObjectRequest jsonObjectRequest = new JsonObjectRequest(Request.Method.POST, url, object,
                new Response.Listener<JSONObject>() {
                    @Override
                    public void onResponse(JSONObject response) {
                        System.out.println("String Response : "+ response.toString());
                        Toast.makeText(getApplicationContext(), "Õnnestus!", Toast.LENGTH_LONG).show();
                    }
                }, new Response.ErrorListener() {
            @Override
            public void onErrorResponse(VolleyError error) {
                System.out.println(error);
                Toast.makeText(getApplicationContext(), "Tekkis viga! Palun proovige uuesti.", Toast.LENGTH_LONG).show();
            }
        });
        jsonObjectRequest.setRetryPolicy(new RetryPolicy() {
            @Override
            public int getCurrentTimeout() {
                return 50000;
            }

            @Override
            public int getCurrentRetryCount() {
                return 50000;
            }

            @Override
            public void retry(VolleyError error) throws VolleyError {

            }
        });
        requestQueue.add(jsonObjectRequest);
    }


}
