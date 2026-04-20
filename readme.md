Project 3: Serverless Task Manager

Aplikasi ini mendemonstrasikan integrasi AWS Amplify, Lambda, API Gateway, dan DynamoDB.

Komponen AWS yang Digunakan:
1.  **DynamoDB:** Menyimpan data tugas.
2.  **Lambda:** Menangani logika bisnis (baca/tulis data).
3.  **API Gateway:** Membuat REST API sebagai pintu masuk.
4.  **Amplify:** Menseploy kode Lambda ini dari GitHub.

Langkah Konfigurasi AWS:

### 1. DynamoDB
-   Buat tabel baru.
-   **Table name:** `LKS_Tasks_Table`
-   **Partition key:** `taskId` (Type: String)
-   Biarkan pengaturan lainnya default.

### 2. Lambda
-   Buat fungsi Lambda baru.
-   **Function name:** `LKS_Task_Handler`
-   **Runtime:** Python 3.x
-   **Permissions:** Ubah default execution role, pilih **Use an existing role**, cari `LabRole` (role ini punya akses ke DynamoDB).
-   Setelah fungsi dibuat, **Copy isi file `app.py`** dari repo ini ke editor kode Lambda. Klik **Deploy**.
-   Masuk ke tab **Configuration** -> **Environment variables**.
-   Klik **Edit** -> **Add environment variable**.
    -   **Key:** `TABLE_NAME`
    -   **Value:** `LKS_Tasks_Table` (Harus sama persis dengan nama tabel DynamoDB yang dibuat).
-   **Save**.

### 3. API Gateway
-   Buat API baru, pilih **REST API** (bukan HTTP API). Klik **Build**.
-   **API name:** `LKS_Task_API` -> **Create**.
-   Klik **Actions** -> **Create Resource**.
    -   **Resource Name:** `tasks`
    -   **Resource Path:** `/tasks`
    -   Centang **Enable API Gateway CORS**.
-   Klik Resource `/tasks` -> **Actions** -> **Create Method**.
    -   Pilih **GET**. Klik centang.
    -   Integration type: **Lambda Function**.
    -   Centang **Use Lambda Proxy integration** (Wajib).
    -   Lambda Function: `LKS_Task_Handler` (pilih fungsi yang tadi dibuat). Klik **Save**.
-   Ulangi langkah di atas, buat Method **POST** untuk Resource `/tasks`. Centang **Lambda Proxy integration**.
-   Sekali lagi, buat Method **OPTIONS** untuk Resource `/tasks`. Centang **Lambda Proxy integration**.
-   Setelah semua method dibuat (GET, POST, OPTIONS), klik pada Resource `/tasks` -> **Actions** -> **Enable CORS**. Centang semua method, klik **Enable CORS and replace existing...**.
-   Klik **Actions** -> **Deploy API**.
    -   **Deployment stage:** `[New Stage]`
    -   **Stage name:** `prod`
-   Ambil **Invoke URL** yang muncul (misal: `https://xyz.execute-api.us-east-1.amazonaws.com/prod`).

### 4. Uji Coba API (Gunakan Postman/Curl)
-   **GET** `https://[INVOKE_URL]/tasks` -> Harus return `[]` (kosong).
-   **POST** `https://[INVOKE_URL]/tasks` dengan Body (JSON): `{"task_name": "Belajar AWS VPC"}` -> Harus return message "Task created".
-   **GET** lagi -> Harus ada data task yang tadi dibuat.

### 5. AWS Amplify (Optional/Jika diminta deploy dari Repo)
-   Aplikasi ini adalah *backend murni*. Jika diminta menggunakan Amplify untuk *deploy frontend* yang memanggil API ini, kamu harus membuat file HTML/JS sederhana dan memasukkan `Invoke URL` API Gateway ke dalam kode JS tersebut, lalu deploy lewat Amplify.

---
*Catatan: File `amplify.yml` di repo ini hanya formalitas agar Amplify tidak error saat build.*