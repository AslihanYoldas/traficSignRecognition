package com.example.kamera3



import android.app.Activity
import android.content.Intent
import android.content.pm.PackageManager
import android.graphics.BitmapFactory
import android.os.Bundle
import android.os.Environment
import android.provider.MediaStore
import android.util.Log
import android.widget.Toast
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.core.content.FileProvider
import com.example.kamera3.databinding.ActivityMainBinding
import okhttp3.MediaType.Companion.toMediaTypeOrNull
import okhttp3.MultipartBody
import okhttp3.OkHttpClient
import okhttp3.RequestBody
import okhttp3.RequestBody.Companion.asRequestBody
import okhttp3.RequestBody.Companion.toRequestBody
import retrofit2.Call
import retrofit2.Callback
import retrofit2.Response
import retrofit2.Retrofit
import retrofit2.converter.gson.GsonConverterFactory
import java.io.File


class MainActivity : AppCompatActivity() {

    private lateinit var binding : ActivityMainBinding
    private lateinit  var photoFile:File

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        val view = binding.root
        setContentView(view)
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.CAMERA) == PackageManager.PERMISSION_DENIED)
            ActivityCompat.requestPermissions(this, arrayOf(android.Manifest.permission.CAMERA), Constant.REQUEST_CODE)



        binding.btnTakePicture.setOnClickListener{

            val takePictureIntent= Intent(MediaStore.ACTION_IMAGE_CAPTURE)
            photoFile=getPhotoFile()
            val fileProvider = FileProvider.getUriForFile(this, "com.example.kamera3.fileprovider", photoFile)
            takePictureIntent.putExtra(MediaStore.EXTRA_OUTPUT,fileProvider)
            startActivityForResult(takePictureIntent, Constant.REQUEST_CODE)

        }
    }
    object ServiceBuilder {

            private val client = OkHttpClient.Builder().build()

            private val retrofit = Retrofit.Builder()
                .baseUrl(Constant.BASE_URL)

                .addConverterFactory(GsonConverterFactory.create())
                .client(client)
                .build()

            fun<T> buildService(service: Class<T>): T{
                return retrofit.create(service)
            }
    }



 private fun getResult() {
     val retrofit = ServiceBuilder.buildService(ApiInterface::class.java)
     val reqFile: RequestBody = photoFile.asRequestBody("image/*".toMediaTypeOrNull())
     val body: MultipartBody.Part =
         MultipartBody.Part.createFormData("attach", photoFile.name, reqFile)
     val name: RequestBody = "upload_test".toRequestBody("text/plain".toMediaTypeOrNull())
     retrofit.postImage(body,name)?.enqueue(
         object : Callback<DenemeRespone> {
             override fun onFailure(call: Call<DenemeRespone>, t: Throwable) {
                 binding.textViewSonuc.setText(R.string.server_hata)
             }

             override fun onResponse(call: Call<DenemeRespone>, response: Response<DenemeRespone>) {
                 val sonuc = response.body()
                 if (sonuc != null) {
                     Log.d("responsee", "" + sonuc.result)
                     binding.textViewSonuc.setText(sonuc.result)
                 }
             }
         })
 }

    private fun getPhotoFile(): File {
        // Use `getExternalFilesDir` on Context to access package-specific directories.
        val storageDirectory = getExternalFilesDir(Environment.DIRECTORY_PICTURES)//We are gonna put to photo here
        return File.createTempFile(Constant.FILE_NAME, ".jpg", storageDirectory)

    }

    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<String>, grantResults: IntArray)
    {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == Constant.REQUEST_CODE) {
            if (grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                    Toast.makeText(this, "camera permission granted", Toast.LENGTH_LONG)
                    .show();
            } else {
                    Toast.makeText(this, "camera permission denied", Toast.LENGTH_LONG)
                    .show();
                         }
                     }

                 }

    override fun onActivityResult(requestCode: Int, resultCode: Int, data: Intent?) {
        //Bunlarin ikisi de dogru ise kullanıcı basarili bir sekilde foto cekmis
        if (requestCode == Constant.REQUEST_CODE && resultCode == Activity.RESULT_OK) {
            //data stores low quality image that user took
            //val takenImage=data?.extras?.get("data") as Bitmap
            val takenImage = BitmapFactory.decodeFile(photoFile.absolutePath)
            binding.imageView.setImageBitmap(takenImage)
            binding.textViewSonuc.setText("Bekleyiniz")
            getResult()


        } else
            super.onActivityResult(requestCode, resultCode, data)
    }


}



