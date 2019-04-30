package com.bargio.firebase;


import android.support.annotation.NonNull;
import android.util.Log;
import com.google.android.gms.tasks.OnCompleteListener;
import com.google.android.gms.tasks.OnSuccessListener;
import com.google.android.gms.tasks.Task;
import com.google.firebase.database.DataSnapshot;
import com.google.firebase.database.DatabaseError;
import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;
import com.google.firebase.database.ValueEventListener;
import com.google.firebase.firestore.FirebaseFirestore;
import com.google.firebase.firestore.QueryDocumentSnapshot;
import com.google.firebase.firestore.QuerySnapshot;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;


public class FirebaseClient {
    //for user data
    static FirebaseDatabase database = FirebaseDatabase.getInstance();
    //for user movements
    static FirebaseFirestore firestore = FirebaseFirestore.getInstance();
    static final String TAG = FirebaseClient.class.getSimpleName();

    private static final String COLLECTION = "users";


    /**
     * Save user details on firebase db (all detail) and on firestore db (only positions)
     * @param userDetails
     *
     */
    public static void firebaseAddUpdateUserDetails(UserDetails userDetails){
        Log.d(TAG,userDetails.toString());
        DatabaseReference dbReference = database.getReference(userDetails.getUsername());
        dbReference.setValue(userDetails);
        firestoreAddUpdateUserDetails(userDetails);
    }

    /**
     * Update user details (user already exist)..principal update last location of users
     * @param userDetails
     */
    public static void firebaseUpdateUserDetails(final UserDetails userDetails){
        //CApire come usare questo metodo
        DatabaseReference dbReference = database.getReference(userDetails.getUsername());
        dbReference.child(userDetails.getUsername()).addValueEventListener(new ValueEventListener() {
            @Override
            public void onDataChange(@NonNull DataSnapshot dataSnapshot) {
                UserDetails userOld = dataSnapshot.getValue(UserDetails.class);
                if(userOld!=null) {
                    Log.d(TAG, userOld.toString());
                }
            }

            @Override
            public void onCancelled(@NonNull DatabaseError databaseError) {

            }
        });
    }

    private static Map mapCreator(UserDetails userDetails){
        Map<String, Object> user = new HashMap<>();
        ArrayList listLocation = new ArrayList();
        listLocation.add(userDetails.getDetails().getLastLocation());
        user.put("username", userDetails.getUsername());
        user.put("locations",listLocation );
        return user;
    }

    /**
     * Add/Update data to firestore (only first registration)
     * @param userDetails
     */
    public static void firestoreAddUpdateUserDetails(final UserDetails userDetails){
        // Create a new user to firestore
        Map<String, Object> user = mapCreator(userDetails);
        // Add a new document with a generated ID
        firestore.collection(COLLECTION).document(userDetails.getUsername()).set(user).addOnSuccessListener(new OnSuccessListener<Void>() {
            @Override
            public void onSuccess(Void aVoid) {
                Log.d(TAG, "DocumentSnapshot added with ID: " + userDetails.getUsername());
            }
        });
    }


    /**
     * read all data from firestore
     * @param userDetails
     */
    public static void firestoreRead(UserDetails userDetails){
        firestore.collection(COLLECTION)
                .get()
                .addOnCompleteListener(new OnCompleteListener<QuerySnapshot>() {
                    @Override
                    public void onComplete(@NonNull Task<QuerySnapshot> task) {
                        if (task.isSuccessful()) {
                            for (QueryDocumentSnapshot document : task.getResult()) {
                                Log.d(TAG, document.getId() + " => " + document.getData());

                            }
                        } else {
                            Log.w(TAG, "Error getting documents.", task.getException());
                        }
                    }
                });
    }

    /**
     * firestore update..calling only after {@link #firestoreRead(UserDetails)}
     * @param userDetails
     * @param document
     */
    private static void firestoreUpdate(UserDetails userDetails, QueryDocumentSnapshot document){
        Map<String, Object> user = document.getData();
        ArrayList locations = (ArrayList)user.get(Details.FIRESTORE_LOCATIONS_ID);
        locations.add(userDetails.getDetails().getLastLocation());
        user.put(Details.FIRESTORE_LOCATIONS_ID, locations);
        firestore.collection(COLLECTION)
                .document(document.getId())
                .update(user);

    }
}
