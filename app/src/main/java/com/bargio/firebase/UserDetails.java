package com.bargio.firebase;

import com.google.firebase.firestore.GeoPoint;

public class UserDetails {
    private String username;
    private boolean isHunter;
    private Details details;

    public UserDetails(String username, String name, String surname, String email, GeoPoint lastLocation, String lastCity, boolean isHunter) {
        this.username = username;
        this.isHunter = isHunter;
        details = new Details(name,surname,email,lastLocation,lastCity);
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public Details getDetails() {
        return details;
    }

    public void setDetails(Details details) {
        this.details = details;
    }

    public boolean getIsHunter() {
        return isHunter;
    }

    public void setIsHunter(boolean isHunter) {
        this.isHunter = isHunter;
    }

    @Override
    public String toString() {
        return "UserDetails{" +
                "username='" + username + '\'' +
                ", isHunter=" + isHunter +
                ", details=" + details +
                '}';
    }
}
