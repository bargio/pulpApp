package com.bargio.pulpapp;

import android.Manifest;
import android.app.Activity;
import android.app.ProgressDialog;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.os.Bundle;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v7.app.AppCompatActivity;
import android.util.Log;

import android.widget.Button;
import android.widget.ImageButton;
import android.widget.Toast;

import com.bargio.listeners.MainButtonListener;
import com.google.android.gms.auth.api.Auth;
import com.facebook.FacebookSdk;
import com.facebook.appevents.AppEventsLogger;

import com.google.android.gms.auth.api.signin.GoogleSignInOptions;
import com.google.android.gms.common.ConnectionResult;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.firebase.auth.FirebaseAuth;



public class MainActivity extends AppCompatActivity implements GoogleApiClient.OnConnectionFailedListener {

    GoogleApiClient mGoogleApiClient;
    MainButtonListener mainButtonListener;
    GoogleSignInOptions gso;

    com.google.android.gms.common.SignInButton signInGoogle;
    ImageButton tutorialButton;

    Button sendButton;
    Button takePicture;
    Button firebaseSender;

    Button firebaseUpdater;

    public  Location locationNew;


    private FirebaseAuth mAuth;
    private LocationManager mLocationManager;

    private final LocationListener mLocationListener = new LocationListener() {
        @Override
        public void onLocationChanged(final Location location) {

            Log.d("Main","cambia location");
            locationNew = location;
        }

        @Override
        public void onStatusChanged(String provider, int status, Bundle extras) {
            Log.d("Main 3","cambia location");
        }

        @Override
        public void onProviderEnabled(String provider) {
            Log.d("Main 2","cambia location");
        }

        @Override
        public void onProviderDisabled(String provider) {
            Log.d("Main 1","cambia location");
        }
    };

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        //mAuth = FirebaseAuth.getInstance();
        FacebookSdk.sdkInitialize(this);

        setContentView(R.layout.activity_main);

        mLocationManager = (LocationManager) getSystemService(LOCATION_SERVICE);

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED && ActivityCompat.checkSelfPermission(this, Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            // TODO: Consider calling
            //    ActivityCompat#requestPermissions
            // here to request the missing permissions, and then overriding
            //   public void onRequestPermissionsResult(int requestCode, String[] permissions,
            //                                          int[] grantResults)
            // to handle the case where the user grants the permission. See the documentation
            // for ActivityCompat#requestPermissions for more details.
            return;
        }
        mLocationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000,
                10, mLocationListener);
        signInGoogle = findViewById(R.id.googleSignInButton);
        tutorialButton = findViewById(R.id.imageButton);
        sendButton = findViewById(R.id.http);
        takePicture = findViewById(R.id.photo);
        firebaseSender = findViewById(R.id.firebase);
        firebaseUpdater = findViewById(R.id.firebaseUpdate);

        inizializer();


        tutorialButton.setOnClickListener(mainButtonListener);
        signInGoogle.setOnClickListener(mainButtonListener);
        sendButton.setOnClickListener(mainButtonListener);
        takePicture.setOnClickListener(mainButtonListener);
        firebaseSender.setOnClickListener(mainButtonListener);
        firebaseUpdater.setOnClickListener(mainButtonListener);

        signInGoogle.setId(MainButtonListener.GOGGLE_BUTTON);
        tutorialButton.setId(MainButtonListener.TUTORIAL_BUTTON);
        sendButton.setId(MainButtonListener.SEND_BUTTON);
        takePicture.setId(MainButtonListener.PHOTO);
        firebaseSender.setId(MainButtonListener.FIREBASE);
        firebaseUpdater.setId(MainButtonListener.FIREBASE_UPDATE);
        isFirstRun();
        delay();
    }


    private void inizializer() {
        Log.d("Initializer","Start");
        gso = new GoogleSignInOptions.Builder(GoogleSignInOptions.DEFAULT_SIGN_IN)
                .requestIdToken(String.valueOf(R.string.server_client_id))
                .requestEmail()
                .build();
        mGoogleApiClient = new GoogleApiClient.Builder(this)
                .enableAutoManage(this /* FragmentActivity */, this /* OnConnectionFailedListener */)
                .addApi(Auth.GOOGLE_SIGN_IN_API, gso)
                .build();

        mainButtonListener = new MainButtonListener(this, mGoogleApiClient);
        Log.d("Initializer","End");


    }


    private void isFirstRun() {
        Boolean isFirstRun = getSharedPreferences("PREFERENCE", MODE_PRIVATE)
                .getBoolean("isFirstRun", true);

        if (isFirstRun) {
            //show sign up activity
            startActivity(new Intent(MainActivity.this, TutorialActivity.class));
            Toast.makeText(MainActivity.this, "Run only once", Toast.LENGTH_LONG)
                    .show();
        }

        getSharedPreferences("PREFERENCE", MODE_PRIVATE).edit()
                .putBoolean("isFirstRun", false).commit();
        }



        public void delay(){
            final ProgressDialog progressDialog = new ProgressDialog(MainActivity.this,
                    R.style.Widget_AppCompat_ProgressBar_Horizontal);
            progressDialog.setIndeterminate(true);
            progressDialog.setMessage("Authenticating...");
            progressDialog.show();
            new android.os.Handler().postDelayed(
                    new Runnable() {
                        public void run() {
                            // On complete call either onLoginSuccess or onLoginFailed
                            Toast.makeText(MainActivity.this,"ciao",Toast.LENGTH_LONG);
                            // onLoginFailed();
                            progressDialog.dismiss();
                        }
                    }, 5000);
        }

    @Override
    public void onConnectionFailed(@NonNull ConnectionResult connectionResult) {

    }
    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {
        if (requestCode == 1888 && resultCode == Activity.RESULT_OK)
        {
            Log.d("MAIN vero","PHOTO");
            Intent intent = new Intent(MainActivity.this, PhotoView.class);

            intent.putExtra("photo",data);
            startActivity(intent);
        }
    }
    @Override
    public void onStart() {
        super.onStart();
        // Check if user is signed in (non-null) and update UI accordingly.
       // FirebaseUser currentUser = mAuth.getCurrentUser();
       // updateUI(currentUser);
    }

}
