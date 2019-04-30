package com.bargio.firebase;

import android.location.Location;

import com.google.android.gms.maps.model.LatLng;
import com.google.firebase.firestore.GeoPoint;

import java.util.ArrayList;
import java.util.List;

public class Details {

    private String name;
    private String surname;
    private String email;
    private GeoPoint lastLocation;
    private String lastCity;
    static final String FIRESTORE_LOCATIONS_ID = "locations";


    public Details(String name, String surname, String email, GeoPoint lastLocation, String lastCity) {
        this.name = name;
        this.surname = surname;
        this.email = email;
        this.lastLocation = lastLocation;
        this.lastCity = lastCity;

    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public String getSurname() {
        return surname;
    }

    public void setSurname(String surname) {
        this.surname = surname;
    }

    public String getEmail() {
        return email;
    }

    public void setEmail(String email) {
        this.email = email;
    }

    public GeoPoint getLastLocation() {
        return lastLocation;
    }

    public void setLastLocation(GeoPoint lastLocation) {
        this.lastLocation = lastLocation;
    }

    public String getLastCity() {
        return lastCity;
    }

    public void setLastCity(String lastCity) {
        this.lastCity = lastCity;
    }


    @Override
    public String toString() {
        return "Details{" +
                "name='" + name + '\'' +
                ", surname='" + surname + '\'' +
                ", email='" + email + '\'' +
                ", lastLocation=" + lastLocation +
                ", lastCity='" + lastCity + '\'' +
                '}';
    }
}
