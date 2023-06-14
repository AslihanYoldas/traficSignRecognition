package com.example.kamera3

import okhttp3.MultipartBody
import okhttp3.RequestBody

import retrofit2.Call


import retrofit2.http.GET
import retrofit2.http.Multipart
import retrofit2.http.POST
import retrofit2.http.Part


//GET REQUEST
interface ApiInterface {

    @Multipart
    @POST("trafikisareti")
    fun postImage(
        @Part image: MultipartBody.Part?,
        @Part("upload_test") name: RequestBody?,
    ): Call<DenemeRespone>?




}
