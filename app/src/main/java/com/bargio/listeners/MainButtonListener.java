package com.bargio.listeners;

import android.app.Activity;
import android.content.Intent;
import android.graphics.Bitmap;
import android.location.Location;
import android.util.Log;
import android.view.View;

import com.bargio.firebase.FirebaseClient;
import com.bargio.firebase.UserDetails;
import com.bargio.pulpapp.MainActivity;
import com.bargio.pulpapp.MapsActivity;
import com.bargio.pulpapp.PhotoView;
import com.bargio.services.HttpClient;
import com.google.android.gms.auth.api.Auth;
import com.google.android.gms.common.api.GoogleApiClient;
import com.google.android.gms.maps.model.LatLng;
import com.google.firebase.firestore.GeoPoint;
import com.loopj.android.http.JsonHttpResponseHandler;

import java.io.ByteArrayOutputStream;

import static com.google.android.gms.auth.api.credentials.CredentialPickerConfig.Prompt.SIGN_IN;

public class MainButtonListener extends Activity implements View.OnClickListener {

    GoogleApiClient mGoogleApiClient;
    MainActivity mainIntent;
    private static final int CAMERA_REQUEST = 1888;

    public static final int GOGGLE_BUTTON = 1;
    public static final int TUTORIAL_BUTTON = 2;
    public static final int SEND_BUTTON = 0;
    public static final int PHOTO = 4;
    public static final int FIREBASE = 5;
    public static final int FIREBASE_UPDATE = 6;

    public MainButtonListener(MainActivity intent, GoogleApiClient mGoogleApiClient){
        this.mGoogleApiClient = mGoogleApiClient;
        this.mainIntent = intent;
    }

    @Override
    public void onClick(View v) {
        Log.d("1","SONO QUA " + v.getId());
        Log.d("1",mGoogleApiClient.toString());

        Log.d("1",mainIntent.toString());

        if(v.getId()==MainButtonListener.GOGGLE_BUTTON){

            Log.d("2","SONO QUA");
            onClickGoogle();
        }else if(v.getId()==MainButtonListener.TUTORIAL_BUTTON){

            Log.d("3","SONO QUA");
            onClickImageView();
        }else if(v.getId()== SEND_BUTTON){
            Log.d("3","Get");
            HttpClient.post("tracks",null,new JsonHttpResponseHandler());
        }else if(v.getId()== PHOTO){
            Log.d("4","PHOTO");
            onClickPhoto();
        }else if(v.getId() == FIREBASE){
            Log.d("5","FIREBASE");
            onClickFirebase();
        }else if(v.getId() == FIREBASE_UPDATE){
            Log.d("5","FIREBASE Update");
            onClickFirebaseUpdate();
        }

        switch(v.getId()){
            case GOGGLE_BUTTON:
                break;
            case TUTORIAL_BUTTON:
                break;
        }
    }

    private void onClickPhoto() {
        Intent cameraIntent = new Intent(android.provider.MediaStore.ACTION_IMAGE_CAPTURE);
        mainIntent.startActivityForResult(cameraIntent, CAMERA_REQUEST);
    }

    public void onClickGoogle(){
        Log.d("Google", "Try to login");
        Intent signInIntent = Auth.GoogleSignInApi.getSignInIntent(mGoogleApiClient);
        mainIntent.startActivityForResult(signInIntent, SIGN_IN);
    }
    public void onClickImageView(){
        Log.d("Click","Image view clicked");
        Intent intent = new Intent(mainIntent, MapsActivity.class);
        mainIntent.startActivity(intent);
    }

    public void onClickFirebase(){
        Log.d("Main3",mainIntent.locationNew.toString());
        UserDetails user = new UserDetails("bargio", "gio","bar",
                "gg@gg.it",new GeoPoint(2.14,3.265),"milano", false);//,new GeoPoint(mainIntent.locationNew.getLatitude(),mainIntent.locationNew.getLongitude()));
        FirebaseClient.firebaseAddUpdateUserDetails(user);
    }
    public void onClickFirebaseUpdate(){
        UserDetails user = new UserDetails("bargio", "gio","bar",
                "gg@gg.it",new GeoPoint(2.56,10.68),"milano",true);//,new GeoPoint(mainIntent.locationNew.getLatitude(),mainIntent.locationNew.getLongitude()));
        FirebaseClient.firebaseUpdateUserDetails(user);

    }

    protected void onActivityResult(int requestCode, int resultCode, Intent data)
    {

        Log.d("MAIN","PHOTO");

        Bitmap photo = (Bitmap) data.getExtras().get("data");

        ByteArrayOutputStream bStream = new ByteArrayOutputStream();
        photo.compress(Bitmap.CompressFormat.PNG, 100, bStream);
        byte[] byteArray = bStream.toByteArray();

        Intent intent = new Intent(mainIntent, PhotoView.class);


        intent.putExtra("photo",byteArray);
        startActivity(intent);


    }
}
