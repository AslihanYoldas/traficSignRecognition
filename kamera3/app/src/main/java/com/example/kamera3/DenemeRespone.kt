package com.example.kamera3

import com.google.gson.annotations.SerializedName

data class DenemeRespone(
    @SerializedName("isSuccess")
    var isSuccess: Boolean,

    @SerializedName("result")
    var result: String?

    )
