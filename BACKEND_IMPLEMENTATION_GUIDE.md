# 🚀 دليل تنفيذ الباك اند - Backend Implementation Guide

## 📋 نظرة عامة

هذا الدليل الشامل يوضح لفريق الباك اند كيفية تحويل الموقع من Frontend Static إلى نظام متكامل مع Backend كامل. المشروع هو **نظام أوزريكس - Ozrix System**، نظام ذكي لمراقبة سيارات ذوي الهمم.

---

## 🎯 الهدف من التحويل

### الوضع الحالي (Frontend Only)
- البيانات مخزنة في JavaScript كـ Static Data
- لا يوجد قاعدة بيانات حقيقية
- لا يوجد Authentication حقيقي
- لا يوجد اتصال مع Raspberry Pi
- لا يوجد اتصال مع AI Model

### الوضع المطلوب (Full Stack)
- ✅ قاعدة بيانات حقيقية (MongoDB/PostgreSQL)
- ✅ Authentication & Authorization كامل
- ✅ RESTful API
- ✅ Real-time updates (WebSocket/SSE)
- ✅ ربط مع Raspberry Pi
- ✅ ربط مع AI Model
- ✅ File Storage للصور والفيديوهات
- ✅ Logging & Monitoring

---

## 🏗️ هيكل النظام المطلوب

```
┌─────────────────────────────────────────────────────────────┐
│                    Frontend (Current)                       │
│  HTML + CSS + JavaScript (Vanilla)                         │
│  - index.html, admin/*.html                                │
│  - css/*.css                                                │
│  - js/*.js                                                  │
└──────────────────────┬──────────────────────────────────────┘
                       │ HTTP/WebSocket
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend API Server                       │
│  Node.js/Express أو Python/Flask/FastAPI                    │
│  - Authentication Service                                   │
│  - Violations Service                                       │
│  - Users Service                                            │
│  - Vehicles Service                                         │
│  - Activities Service                                       │
│  - File Upload Service                                      │
└──────────────────────┬──────────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        ▼              ▼              ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│   Database   │ │  File Store  │ │  AI Service  │
│  MongoDB/    │ │  AWS S3/     │ │  TensorFlow  │
│  PostgreSQL  │ │  Local FS    │ │  /PyTorch    │
└──────────────┘ └──────────────┘ └──────────────┘
        │              │              │
        └──────────────┼──────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│              External Services                              │
│  - Raspberry Pi (Radar Devices)                            │
│  - AI Model (Face Recognition, Plate Detection)            │
│  - Email Service (Notifications)                           │
└─────────────────────────────────────────────────────────────┘
```

---

## 📊 هيكل البيانات (Data Models)

### 1. User Model (المستخدمين)

```javascript
{
  _id: ObjectId,
  id: Number,                    // 1, 2, 3, ...
  name: String,                  // "محمود أيمن"
  email: String,                 // "mahmoud@ozrix.com"
  password: String,              // Hashed password
  phone: String,                 // "01012345678"
  nationalId: String,            // "29801151234567"
  role: String,                  // "مدير تنفيذي"
  roleType: String,              // "executive" | "employee" | "traffic_officer"
  code: String,                  // "EXC-001"
  avatar: String,                // URL to avatar image
  status: String,                // "online" | "offline"
  lastSeen: String,              // "متصل الآن" | "آخر ظهور منذ..."
  joinDate: Date,                // "2024-01-01"
  department: String,            // "الإدارة التنفيذية"
  violationsHandled: Number,     // 245
  hoursWorked: Number,           // 1840
  location: String,              // "القاهرة - المقر الرئيسي"
  createdAt: Date,
  updatedAt: Date,
  refreshToken: String,          // For JWT refresh
  isActive: Boolean              // true
}
```

### 2. Vehicle/Owner Model (السيارات وأصحابها)

```javascript
{
  _id: ObjectId,
  ownerId: Number,               // 333, 111, 777, ...
  ownerName: String,             // "محمود أحمد محمد"
  ownerNameKey: String,           // "nameMahmoudAhmedMohamed" (for i18n)
  ownerAvatar: String,           // URL to avatar
  initials: String,              // "م أ م"
  nationalId: String,           // "29801151234567"
  location: String,             // "رادار شبرا – بنها (الكيلو 25)"
  car: {
    brand: String,               // "أودي"
    brandKey: String,            // "brandAudi"
    model: String,               // "A4"
    modelKey: String,           // "modelA4"
    modelLabel: String,          // "A4 2022"
    plate: String,              // "ا ٥٥"
    color: String               // "رمادي"
  },
  companions: [
    {
      relationKey: String,       // "wife", "son", "daughter", ...
      nameKey: String,          // "nameFatimaMahmoud"
      profileImg: String,       // URL to image
      idCard: String,           // URL to ID card image
      nationalId: String,       // Companion's national ID
      relation: String          // "زوجة", "ابن", ...
    }
  ],
  serviceCard: String,          // URL to service card image
  createdAt: Date,
  updatedAt: Date
}
```

### 3. Violation Model (المخالفات)

```javascript
{
  _id: ObjectId,
  id: String,                    // "V-333", "V-111", ...
  type: String,                  // "car" | "radar"
  location: String,              // "رادار شبرا – بنها (الكيلو 25)"
  image: String,                 // URL to violation image
  video: String,                 // URL to violation video (optional)
  date: String,                  // "2024-02-01"
  time: String,                  // "08:40"
  timestamp: Date,                // Full datetime
  status: String,                // "pending" | "confirmed" | "rejected" | "completed"
  detectedPersons: Number,       // 1, 2, 3, ...
  dangerLevel: String,          // "low" | "medium" | "high" (optional)
  carNumber: String,             // "ا ٥٥"
  ownerId: Number,               // Reference to owner
  ownerName: String,             // "محمود أحمد محمد"
  deviceId: String,              // "RADAR_001" (from Raspberry Pi)
  aiConfidence: Number,          // 0.95 (from AI model)
  faceMatch: Boolean,            // true/false (from AI)
  ownerMatch: Boolean,           // true/false (from AI)
  reviewedBy: ObjectId,          // User ID who reviewed
  reviewedAt: Date,              // When reviewed
  reviewNote: String,            // Optional note
  publishedToHome: Boolean,      // false
  appeal: {
    submitted: Boolean,          // false
    submittedAt: Date,
    reason: String,
    attachments: [String],       // URLs to files
    status: String,              // "pending" | "approved" | "rejected"
    reviewedBy: ObjectId,
    reviewedAt: Date
  },
  createdAt: Date,
  updatedAt: Date
}
```

### 4. Activity Model (سجل الأنشطة)

```javascript
{
  _id: ObjectId,
  id: Number,                    // 1, 2, 3, ...
  action: String,                // "تأكيد مخالفة", "رفض مخالفة", ...
  user: String,                  // "أحمد ياسر"
  userId: ObjectId,              // Reference to User
  time: String,                  // "منذ 5 دقائق"
  timestamp: Date,               // Full datetime
  type: String,                  // "success" | "danger" | "warning" | "info"
  details: String,               // "مخالفة رقم V-333"
  violationId: ObjectId,        // Reference to Violation (optional)
  metadata: Object               // Additional data
}
```

### 5. Device Model (أجهزة الرادار)

```javascript
{
  _id: ObjectId,
  deviceId: String,              // "RADAR_001"
  name: String,                  // "رادار شبرا – بنها"
  location: String,              // "رادار شبرا – بنها (الكيلو 25)"
  coordinates: {
    lat: Number,
    lng: Number
  },
  status: String,                // "active" | "inactive" | "maintenance"
  lastSeen: Date,                // Last ping from device
  apiKey: String,                // Hashed API key for device
  violationsCount: Number,       // Total violations detected
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🔌 API Endpoints المطلوبة

### Base URL
```
Production: https://api.ozrix.com/api/v1
Development: http://localhost:5000/api/v1
```

### Authentication Endpoints

#### 1. تسجيل الدخول
```http
POST /api/v1/auth/login
Content-Type: application/json

Request Body:
{
  "email": "mahmoud@ozrix.com",
  "password": "password123",
  "rememberMe": true
}

Response (200):
{
  "success": true,
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "refreshToken": "refresh_token_here",
  "user": {
    "id": 1,
    "name": "محمود أيمن",
    "email": "mahmoud@ozrix.com",
    "role": "مدير تنفيذي",
    "roleType": "executive",
    "code": "EXC-001",
    "avatar": "assets/img/ceo.jpg"
  }
}
```

#### 2. تسجيل الخروج
```http
POST /api/v1/auth/logout
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "message": "تم تسجيل الخروج بنجاح"
}
```

#### 3. تحديث Token
```http
POST /api/v1/auth/refresh
Content-Type: application/json

Request Body:
{
  "refreshToken": "refresh_token_here"
}

Response (200):
{
  "success": true,
  "token": "new_token_here"
}
```

#### 4. إنشاء حساب جديد
```http
POST /api/v1/auth/signup
Content-Type: application/json

Request Body:
{
  "name": "أحمد محمد",
  "email": "ahmed@ozrix.com",
  "password": "password123",
  "confirmPassword": "password123",
  "phone": "01012345678",
  "nationalId": "29801151234567",
  "roleType": "employee"
}

Response (201):
{
  "success": true,
  "message": "تم إنشاء الحساب بنجاح",
  "user": { ... }
}
```

### Violations Endpoints

#### 5. جلب جميع المخالفات
```http
GET /api/v1/violations
Authorization: Bearer {token}
Query Parameters:
  - status: "pending" | "confirmed" | "rejected" | "completed"
  - type: "car" | "radar"
  - location: "رادار شبرا – بنها"
  - page: 1
  - limit: 20
  - sortBy: "date" | "time" | "status"
  - sortOrder: "asc" | "desc"

Response (200):
{
  "success": true,
  "data": [
    {
      "id": "V-333",
      "type": "car",
      "location": "رادار شبرا – بنها (الكيلو 25)",
      "image": "https://cdn.ozrix.com/violations/v-333.jpg",
      "date": "2024-02-01",
      "time": "08:40",
      "status": "confirmed",
      "carNumber": "ا ٥٥",
      "ownerId": 333,
      "ownerName": "محمود أحمد محمد"
    },
    ...
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 150,
    "totalPages": 8
  }
}
```

#### 6. جلب مخالفة واحدة
```http
GET /api/v1/violations/:id
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": {
    "id": "V-333",
    "type": "car",
    "location": "رادار شبرا – بنها (الكيلو 25)",
    "image": "https://cdn.ozrix.com/violations/v-333.jpg",
    "date": "2024-02-01",
    "time": "08:40",
    "status": "confirmed",
    "carNumber": "ا ٥٥",
    "ownerId": 333,
    "ownerName": "محمود أحمد محمد",
    "detectedPersons": 1,
    "aiConfidence": 0.95,
    "faceMatch": false,
    "ownerMatch": false,
    "reviewedBy": {
      "id": 3,
      "name": "أحمد ياسر"
    },
    "reviewedAt": "2024-02-01T09:00:00Z"
  }
}
```

#### 7. إنشاء مخالفة جديدة (من Raspberry Pi)
```http
POST /api/v1/violations
Authorization: Bearer {device_api_key}
Content-Type: application/json

Request Body:
{
  "deviceId": "RADAR_001",
  "location": "رادار شبرا – بنها (الكيلو 25)",
  "type": "radar",
  "date": "2024-02-01",
  "time": "08:40",
  "timestamp": "2024-02-01T08:40:00Z",
  "carNumber": "ا ٥٥",
  "image": "base64_encoded_image_string",
  "video": "base64_encoded_video_string", // optional
  "aiConfidence": 0.95,
  "faceMatch": false,
  "ownerMatch": false,
  "detectedPersons": 1
}

Response (201):
{
  "success": true,
  "violationId": "V-333",
  "message": "تم استلام المخالفة بنجاح"
}
```

#### 8. تحديث حالة المخالفة
```http
PUT /api/v1/violations/:id
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "status": "confirmed", // "pending" | "confirmed" | "rejected" | "completed"
  "reviewNote": "تم التأكيد بعد المراجعة",
  "publishToHome": true // optional
}

Response (200):
{
  "success": true,
  "message": "تم تحديث المخالفة بنجاح",
  "data": { ... }
}
```

#### 9. رفض مخالفة
```http
POST /api/v1/violations/:id/reject
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "note": "المخالفة غير صحيحة"
}

Response (200):
{
  "success": true,
  "message": "تم رفض المخالفة"
}
```

#### 10. نشر مخالفة في الصفحة الرئيسية
```http
POST /api/v1/violations/:id/publish
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "message": "تم نشر المخالفة في الصفحة الرئيسية"
}
```

### Vehicles/Owners Endpoints

#### 11. جلب جميع السيارات/أصحابها
```http
GET /api/v1/vehicles
Authorization: Bearer {token}
Query Parameters:
  - search: "محمود" // Search by name or plate
  - page: 1
  - limit: 20

Response (200):
{
  "success": true,
  "data": [
    {
      "ownerId": 333,
      "ownerName": "محمود أحمد محمد",
      "nationalId": "29801151234567",
      "car": {
        "brand": "أودي",
        "model": "A4",
        "plate": "ا ٥٥",
        "color": "رمادي"
      },
      "companions": [ ... ]
    },
    ...
  ],
  "pagination": { ... }
}
```

#### 12. جلب سيارة/صاحب واحد
```http
GET /api/v1/vehicles/:ownerId
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": {
    "ownerId": 333,
    "ownerName": "محمود أحمد محمد",
    "nationalId": "29801151234567",
    "avatar": "https://cdn.ozrix.com/avatars/333.jpg",
    "car": { ... },
    "companions": [ ... ],
    "serviceCard": "https://cdn.ozrix.com/cards/333.jpg"
  }
}
```

#### 13. إنشاء/تسجيل سيارة جديدة
```http
POST /api/v1/vehicles
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "ownerName": "محمود أحمد محمد",
  "nationalId": "29801151234567",
  "phone": "01012345678",
  "car": {
    "brand": "أودي",
    "model": "A4",
    "plate": "ا ٥٥",
    "color": "رمادي"
  },
  "companions": [
    {
      "name": "فاطمة محمود",
      "relation": "زوجة",
      "nationalId": "29801151234568",
      "profileImg": "base64_image",
      "idCard": "base64_image"
    }
  ],
  "serviceCard": "base64_image",
  "ownerAvatar": "base64_image"
}

Response (201):
{
  "success": true,
  "ownerId": 333,
  "message": "تم تسجيل السيارة بنجاح"
}
```

#### 14. تحديث بيانات سيارة
```http
PUT /api/v1/vehicles/:ownerId
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "ownerName": "محمود أحمد محمد",
  "phone": "01012345678",
  "car": { ... },
  "companions": [ ... ]
}

Response (200):
{
  "success": true,
  "message": "تم تحديث البيانات بنجاح"
}
```

### Users Endpoints

#### 15. جلب جميع المستخدمين
```http
GET /api/v1/users
Authorization: Bearer {token}
Query Parameters:
  - roleType: "executive" | "employee" | "traffic_officer"
  - status: "online" | "offline"
  - search: "محمود"

Response (200):
{
  "success": true,
  "data": [
    {
      "id": 1,
      "name": "محمود أيمن",
      "email": "mahmoud@ozrix.com",
      "role": "مدير تنفيذي",
      "roleType": "executive",
      "code": "EXC-001",
      "avatar": "assets/img/ceo.jpg",
      "status": "online",
      "lastSeen": "متصل الآن",
      "violationsHandled": 245,
      "hoursWorked": 1840
    },
    ...
  ]
}
```

#### 16. جلب مستخدم واحد
```http
GET /api/v1/users/:id
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": {
    "id": 1,
    "name": "محمود أيمن",
    "email": "mahmoud@ozrix.com",
    "phone": "01012345678",
    "nationalId": "29801151234567",
    "role": "مدير تنفيذي",
    "roleType": "executive",
    "code": "EXC-001",
    "avatar": "assets/img/ceo.jpg",
    "status": "online",
    "lastSeen": "متصل الآن",
    "joinDate": "2024-01-01",
    "department": "الإدارة التنفيذية",
    "violationsHandled": 245,
    "hoursWorked": 1840,
    "location": "القاهرة - المقر الرئيسي"
  }
}
```

#### 17. تحديث حالة المستخدم (Online/Offline)
```http
PUT /api/v1/users/:id/status
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "status": "online" // "online" | "offline"
}

Response (200):
{
  "success": true,
  "message": "تم تحديث الحالة"
}
```

### Activities Endpoints

#### 18. جلب سجل الأنشطة
```http
GET /api/v1/activities
Authorization: Bearer {token}
Query Parameters:
  - type: "success" | "danger" | "warning" | "info"
  - userId: 1
  - action: "تأكيد مخالفة"
  - page: 1
  - limit: 50

Response (200):
{
  "success": true,
  "data": [
    {
      "id": 1,
      "action": "تأكيد مخالفة",
      "user": "أحمد ياسر",
      "userId": 3,
      "time": "منذ 5 دقائق",
      "timestamp": "2024-02-01T10:00:00Z",
      "type": "success",
      "details": "مخالفة رقم V-333",
      "violationId": "V-333"
    },
    ...
  ],
  "pagination": { ... }
}
```

#### 19. إنشاء نشاط جديد
```http
POST /api/v1/activities
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "action": "تأكيد مخالفة",
  "type": "success",
  "details": "مخالفة رقم V-333",
  "violationId": "V-333"
}

Response (201):
{
  "success": true,
  "activityId": 1
}
```

### Devices Endpoints

#### 20. جلب جميع الأجهزة
```http
GET /api/v1/devices
Authorization: Bearer {token}

Response (200):
{
  "success": true,
  "data": [
    {
      "deviceId": "RADAR_001",
      "name": "رادار شبرا – بنها",
      "location": "رادار شبرا – بنها (الكيلو 25)",
      "status": "active",
      "lastSeen": "2024-02-01T10:00:00Z",
      "violationsCount": 512
    },
    ...
  ]
}
```

#### 21. تحديث حالة الجهاز
```http
PUT /api/v1/devices/:deviceId/status
Authorization: Bearer {device_api_key}
Content-Type: application/json

Request Body:
{
  "status": "active" // "active" | "inactive" | "maintenance"
}

Response (200):
{
  "success": true
}
```

### File Upload Endpoints

#### 22. رفع صورة
```http
POST /api/v1/upload/image
Authorization: Bearer {token}
Content-Type: multipart/form-data

Request Body:
  file: [image file]
  type: "violation" | "avatar" | "idCard" | "serviceCard"

Response (200):
{
  "success": true,
  "url": "https://cdn.ozrix.com/images/violation_123.jpg",
  "filename": "violation_123.jpg"
}
```

#### 23. رفع فيديو
```http
POST /api/v1/upload/video
Authorization: Bearer {token}
Content-Type: multipart/form-data

Request Body:
  file: [video file]
  type: "violation"

Response (200):
{
  "success": true,
  "url": "https://cdn.ozrix.com/videos/violation_123.mp4",
  "filename": "violation_123.mp4"
}
```

### Appeal Endpoints

#### 24. تقديم استئناف
```http
POST /api/v1/violations/:id/appeal
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "reason": "المخالفة غير صحيحة",
  "attachments": ["url1", "url2"]
}

Response (201):
{
  "success": true,
  "appealId": "APP-001",
  "message": "تم تقديم الاستئناف بنجاح"
}
```

#### 25. جلب جميع الاستئنافات
```http
GET /api/v1/appeals
Authorization: Bearer {token}
Query Parameters:
  - status: "pending" | "approved" | "rejected"

Response (200):
{
  "success": true,
  "data": [ ... ]
}
```

---

## 🔐 Authentication & Authorization

### JWT Token Structure

```javascript
// Access Token (expires in 15 minutes)
{
  "userId": 1,
  "email": "mahmoud@ozrix.com",
  "roleType": "executive",
  "iat": 1234567890,
  "exp": 1234568790
}

// Refresh Token (expires in 7 days)
{
  "userId": 1,
  "tokenId": "uuid",
  "iat": 1234567890,
  "exp": 1234571490
}
```

### Role-Based Access Control (RBAC)

#### Executive (مدير تنفيذي)
- ✅ جميع الصلاحيات
- ✅ عرض جميع المخالفات
- ✅ تأكيد/رفض المخالفات
- ✅ نشر المخالفات
- ✅ إدارة المستخدمين
- ✅ إدارة السيارات
- ✅ عرض جميع الإحصائيات

#### Traffic Officer (ضابط مرور)
- ✅ عرض المخالفات
- ✅ تأكيد/رفض المخالفات
- ✅ عرض قاعدة البيانات
- ✅ عرض السجل
- ❌ نشر المخالفات
- ❌ إدارة المستخدمين

#### Employee (موظف)
- ✅ عرض المخالفات
- ✅ معالجة المخالفات
- ✅ عرض قاعدة البيانات (قراءة فقط)
- ❌ تأكيد/رفض المخالفات
- ❌ إدارة المستخدمين

### Middleware للتحقق من الصلاحيات

```javascript
// Example: Express.js middleware
const checkRole = (...allowedRoles) => {
  return (req, res, next) => {
    const userRole = req.user.roleType;
    
    if (!allowedRoles.includes(userRole)) {
      return res.status(403).json({
        success: false,
        message: "ليس لديك صلاحية للوصول إلى هذا المورد"
      });
    }
    
    next();
  };
};

// Usage
router.put('/violations/:id', 
  authenticateToken, 
  checkRole('executive', 'traffic_officer'),
  updateViolation
);
```

---

## 🗄️ Database Schema

### MongoDB Collections

#### users
```javascript
{
  _id: ObjectId,
  id: Number,
  name: String,
  email: String (unique, indexed),
  password: String (hashed),
  phone: String,
  nationalId: String (unique, indexed),
  role: String,
  roleType: String (indexed),
  code: String (unique),
  avatar: String,
  status: String,
  lastSeen: String,
  joinDate: Date,
  department: String,
  violationsHandled: Number,
  hoursWorked: Number,
  location: String,
  refreshToken: String,
  isActive: Boolean,
  createdAt: Date (indexed),
  updatedAt: Date
}
```

#### vehicles
```javascript
{
  _id: ObjectId,
  ownerId: Number (unique, indexed),
  ownerName: String,
  ownerNameKey: String,
  ownerAvatar: String,
  initials: String,
  nationalId: String (unique, indexed),
  location: String,
  car: {
    brand: String,
    brandKey: String,
    model: String,
    modelKey: String,
    modelLabel: String,
    plate: String (indexed),
    color: String
  },
  companions: [{
    relationKey: String,
    nameKey: String,
    profileImg: String,
    idCard: String,
    nationalId: String,
    relation: String
  }],
  serviceCard: String,
  createdAt: Date,
  updatedAt: Date
}
```

#### violations
```javascript
{
  _id: ObjectId,
  id: String (unique, indexed),
  type: String (indexed),
  location: String,
  image: String,
  video: String,
  date: String (indexed),
  time: String,
  timestamp: Date (indexed),
  status: String (indexed),
  detectedPersons: Number,
  dangerLevel: String,
  carNumber: String (indexed),
  ownerId: Number (indexed),
  ownerName: String,
  deviceId: String (indexed),
  aiConfidence: Number,
  faceMatch: Boolean,
  ownerMatch: Boolean,
  reviewedBy: ObjectId,
  reviewedAt: Date,
  reviewNote: String,
  publishedToHome: Boolean (indexed),
  appeal: {
    submitted: Boolean,
    submittedAt: Date,
    reason: String,
    attachments: [String],
    status: String,
    reviewedBy: ObjectId,
    reviewedAt: Date
  },
  createdAt: Date (indexed),
  updatedAt: Date
}
```

#### activities
```javascript
{
  _id: ObjectId,
  id: Number,
  action: String,
  user: String,
  userId: ObjectId (indexed),
  time: String,
  timestamp: Date (indexed),
  type: String (indexed),
  details: String,
  violationId: ObjectId (indexed),
  metadata: Object,
  createdAt: Date
}
```

#### devices
```javascript
{
  _id: ObjectId,
  deviceId: String (unique, indexed),
  name: String,
  location: String,
  coordinates: {
    lat: Number,
    lng: Number
  },
  status: String (indexed),
  lastSeen: Date,
  apiKey: String (hashed),
  violationsCount: Number,
  createdAt: Date,
  updatedAt: Date
}
```

---

## 🔄 Real-time Updates

### WebSocket Events

#### Server to Client Events

```javascript
// New violation detected
socket.emit('violation:new', {
  id: "V-333",
  type: "radar",
  location: "رادار شبرا – بنها",
  carNumber: "ا ٥٥",
  timestamp: "2024-02-01T08:40:00Z"
});

// Violation status updated
socket.emit('violation:updated', {
  id: "V-333",
  status: "confirmed",
  reviewedBy: "أحمد ياسر"
});

// User status changed
socket.emit('user:status', {
  userId: 1,
  status: "online",
  lastSeen: "متصل الآن"
});

// New activity
socket.emit('activity:new', {
  id: 1,
  action: "تأكيد مخالفة",
  user: "أحمد ياسر",
  type: "success"
});
```

#### Client to Server Events

```javascript
// Join user room
socket.emit('user:join', {
  userId: 1,
  roleType: "executive"
});

// Leave user room
socket.emit('user:leave', {
  userId: 1
});
```

### Server-Sent Events (SSE) Alternative

```javascript
// Endpoint for SSE
GET /api/v1/events/stream
Authorization: Bearer {token}

// Client connects and receives events
const eventSource = new EventSource('/api/v1/events/stream?token=...');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  // Handle event
};
```

---

## 🔗 ربط Frontend مع Backend

### 1. إنشاء API Service في JavaScript

```javascript
// js/api.js
class ApiService {
  constructor() {
    this.baseURL = process.env.API_URL || 'http://localhost:5000/api/v1';
    this.token = localStorage.getItem('token');
    this.refreshToken = localStorage.getItem('refreshToken');
  }

  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const config = {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        ...(this.token && { 'Authorization': `Bearer ${this.token}` }),
        ...options.headers
      }
    };

    try {
      const response = await fetch(url, config);
      
      // Handle token refresh
      if (response.status === 401) {
        await this.refreshAccessToken();
        config.headers['Authorization'] = `Bearer ${this.token}`;
        return fetch(url, config);
      }

      const data = await response.json();
      
      if (!response.ok) {
        throw new Error(data.message || 'حدث خطأ');
      }

      return data;
    } catch (error) {
      console.error('API Error:', error);
      throw error;
    }
  }

  async refreshAccessToken() {
    try {
      const response = await fetch(`${this.baseURL}/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refreshToken: this.refreshToken })
      });

      const data = await response.json();
      
      if (data.success) {
        this.token = data.token;
        localStorage.setItem('token', data.token);
      }
    } catch (error) {
      // Redirect to login
      window.location.href = '/admin/login.html';
    }
  }

  // Authentication
  async login(email, password, rememberMe) {
    return this.request('/auth/login', {
      method: 'POST',
      body: JSON.stringify({ email, password, rememberMe })
    });
  }

  async logout() {
    return this.request('/auth/logout', { method: 'POST' });
  }

  // Violations
  async getViolations(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/violations?${params}`);
  }

  async getViolation(id) {
    return this.request(`/violations/${id}`);
  }

  async updateViolation(id, data) {
    return this.request(`/violations/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data)
    });
  }

  async confirmViolation(id) {
    return this.updateViolation(id, { status: 'confirmed' });
  }

  async rejectViolation(id, note) {
    return this.request(`/violations/${id}/reject`, {
      method: 'POST',
      body: JSON.stringify({ note })
    });
  }

  // Vehicles
  async getVehicles(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/vehicles?${params}`);
  }

  async getVehicle(ownerId) {
    return this.request(`/vehicles/${ownerId}`);
  }

  // Users
  async getUsers(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/users?${params}`);
  }

  async getUser(id) {
    return this.request(`/users/${id}`);
  }

  // Activities
  async getActivities(filters = {}) {
    const params = new URLSearchParams(filters);
    return this.request(`/activities?${params}`);
  }

  // File Upload
  async uploadImage(file, type) {
    const formData = new FormData();
    formData.append('file', file);
    formData.append('type', type);

    return this.request('/upload/image', {
      method: 'POST',
      headers: {}, // Let browser set Content-Type for FormData
      body: formData
    });
  }
}

// Export singleton instance
window.api = new ApiService();
```

### 2. تحديث صفحات.js لاستخدام API

```javascript
// js/pages.js - Update loadHomePage function

async function loadHomePage() {
  const homeContainer = document.getElementById('homeContainer');
  if (!homeContainer) return;

  try {
    // Show loading
    homeContainer.innerHTML = '<div class="loading">جاري التحميل...</div>';

    // Fetch violations from API
    const response = await window.api.getViolations({
      status: 'pending',
      limit: 20,
      sortBy: 'timestamp',
      sortOrder: 'desc'
    });

    if (response.success) {
      const violations = response.data;
      
      // Render violations
      renderViolations(violations);
    }
  } catch (error) {
    console.error('Error loading violations:', error);
    homeContainer.innerHTML = '<div class="error">حدث خطأ في تحميل البيانات</div>';
  }
}

// Update confirmViolation function
async function confirmViolation(violationId) {
  try {
    const response = await window.api.confirmViolation(violationId);
    
    if (response.success) {
      // Show success message
      showNotification('تم تأكيد المخالفة بنجاح', 'success');
      
      // Reload violations
      loadHomePage();
      
      // Create activity
      await window.api.request('/activities', {
        method: 'POST',
        body: JSON.stringify({
          action: 'تأكيد مخالفة',
          type: 'success',
          details: `مخالفة رقم ${violationId}`,
          violationId: violationId
        })
      });
    }
  } catch (error) {
    showNotification('حدث خطأ في تأكيد المخالفة', 'error');
  }
}
```

### 3. إعداد WebSocket للـ Real-time Updates

```javascript
// js/realtime.js
class RealtimeService {
  constructor() {
    this.socket = null;
    this.token = localStorage.getItem('token');
  }

  connect() {
    const wsURL = process.env.WS_URL || 'ws://localhost:5000';
    
    this.socket = new WebSocket(`${wsURL}?token=${this.token}`);

    this.socket.onopen = () => {
      console.log('WebSocket connected');
      
      // Join user room
      const user = JSON.parse(localStorage.getItem('user'));
      this.socket.send(JSON.stringify({
        type: 'user:join',
        data: { userId: user.id, roleType: user.roleType }
      }));
    };

    this.socket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      this.handleMessage(message);
    };

    this.socket.onerror = (error) => {
      console.error('WebSocket error:', error);
    };

    this.socket.onclose = () => {
      console.log('WebSocket disconnected');
      // Reconnect after 5 seconds
      setTimeout(() => this.connect(), 5000);
    };
  }

  handleMessage(message) {
    switch (message.type) {
      case 'violation:new':
        this.handleNewViolation(message.data);
        break;
      case 'violation:updated':
        this.handleViolationUpdate(message.data);
        break;
      case 'user:status':
        this.handleUserStatus(message.data);
        break;
      case 'activity:new':
        this.handleNewActivity(message.data);
        break;
    }
  }

  handleNewViolation(violation) {
    // Add violation to grid
    if (typeof addViolationToGrid === 'function') {
      addViolationToGrid(violation);
    }
    
    // Show notification
    showNotification(`مخالفة جديدة: ${violation.carNumber}`, 'info');
  }

  handleViolationUpdate(violation) {
    // Update violation in grid
    if (typeof updateViolationInGrid === 'function') {
      updateViolationInGrid(violation);
    }
  }

  handleUserStatus(data) {
    // Update user status in UI
    const userCard = document.querySelector(`[data-user-id="${data.userId}"]`);
    if (userCard) {
      userCard.classList.remove('online', 'offline');
      userCard.classList.add(data.status);
    }
  }

  handleNewActivity(activity) {
    // Add activity to activities list
    if (typeof addActivityToList === 'function') {
      addActivityToList(activity);
    }
  }

  disconnect() {
    if (this.socket) {
      this.socket.close();
    }
  }
}

// Initialize on page load
window.realtime = new RealtimeService();
if (localStorage.getItem('token')) {
  window.realtime.connect();
}
```

---

## 🤖 ربط Raspberry Pi

### 1. API Key للجهاز

كل جهاز Raspberry Pi يحتاج إلى API Key فريد:

```javascript
// Generate API Key for device
POST /api/v1/devices
Authorization: Bearer {admin_token}
Content-Type: application/json

Request Body:
{
  "deviceId": "RADAR_001",
  "name": "رادار شبرا – بنها",
  "location": "رادار شبرا – بنها (الكيلو 25)",
  "coordinates": {
    "lat": 30.0444,
    "lng": 31.2357
  }
}

Response (201):
{
  "success": true,
  "apiKey": "device_api_key_here",
  "message": "تم إنشاء الجهاز بنجاح"
}
```

### 2. Python Code على Raspberry Pi

```python
# violation_sender.py (Updated)
import requests
import json
import base64
from datetime import datetime
from config import API_CONFIG

class ViolationSender:
    def __init__(self):
        self.api_url = API_CONFIG["base_url"]
        self.api_key = API_CONFIG["api_key"]  # Device API Key
        self.device_id = API_CONFIG["device_id"]
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
            "X-Device-ID": self.device_id
        }
    
    def encode_image(self, image_path):
        """Convert image to Base64"""
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode('utf-8')
    
    def send_violation(self, violation_data, image_path, video_path=None):
        """Send violation to server"""
        
        payload = {
            "deviceId": self.device_id,
            "location": API_CONFIG["location"],
            "type": "radar",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "time": datetime.now().strftime("%H:%M:%S"),
            "timestamp": datetime.now().isoformat(),
            "carNumber": violation_data.get("plate_number", ""),
            "image": self.encode_image(image_path),
            "aiConfidence": violation_data.get("confidence", 0),
            "faceMatch": violation_data.get("face_match", False),
            "ownerMatch": violation_data.get("owner_match", False),
            "detectedPersons": violation_data.get("detected_persons", 1)
        }
        
        # Add video if available
        if video_path:
            payload["video"] = self.encode_image(video_path)  # Same encoding for video
        
        try:
            response = requests.post(
                f"{self.api_url}/violations",
                headers=self.headers,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 201:
                result = response.json()
                print(f"✅ Violation sent: {result.get('violationId')}")
                return True
            else:
                print(f"❌ Failed: {response.status_code} - {response.text}")
                self.save_offline(payload)
                return False
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Connection error: {e}")
            self.save_offline(payload)
            return False
    
    def update_device_status(self, status="active"):
        """Update device status (heartbeat)"""
        try:
            response = requests.put(
                f"{self.api_url}/devices/{self.device_id}/status",
                headers=self.headers,
                json={"status": status},
                timeout=10
            )
            return response.status_code == 200
        except:
            return False
```

### 3. Heartbeat Mechanism

```python
# main.py (Updated)
import time
from violation_sender import ViolationSender

class OzrixRadar:
    def __init__(self):
        self.sender = ViolationSender()
        self.heartbeat_interval = 60  # Send heartbeat every 60 seconds
    
    def start(self):
        """Start monitoring"""
        print("🎥 Starting monitoring...")
        
        # Start heartbeat thread
        import threading
        heartbeat_thread = threading.Thread(target=self.heartbeat_loop)
        heartbeat_thread.daemon = True
        heartbeat_thread.start()
        
        # Main monitoring loop
        while True:
            # Capture and analyze
            result = self.detect_violation()
            
            if result["violation_detected"]:
                self.sender.send_violation(result, "image.jpg", "video.mp4")
            
            time.sleep(2)
    
    def heartbeat_loop(self):
        """Send periodic heartbeat"""
        while True:
            self.sender.update_device_status("active")
            time.sleep(self.heartbeat_interval)
```

---

## 🧠 ربط AI Model

### 1. AI Service Endpoint

```http
POST /api/v1/ai/analyze
Authorization: Bearer {device_api_key}
Content-Type: application/json

Request Body:
{
  "image": "base64_encoded_image",
  "type": "violation" // "violation" | "face" | "plate"
}

Response (200):
{
  "success": true,
  "data": {
    "plate_detected": true,
    "plate_number": "ا ٥٥",
    "plate_confidence": 0.95,
    "face_detected": true,
    "face_match": false,
    "owner_match": false,
    "matched_person_id": null,
    "confidence": 0.92
  }
}
```

### 2. Face Recognition Endpoint

```http
POST /api/v1/ai/recognize-face
Authorization: Bearer {device_api_key}
Content-Type: application/json

Request Body:
{
  "image": "base64_encoded_image",
  "vehicle_plate": "ا ٥٥"
}

Response (200):
{
  "success": true,
  "data": {
    "face_detected": true,
    "match_found": true,
    "matched_person_id": 333,
    "matched_person_name": "محمود أحمد محمد",
    "confidence": 0.88,
    "is_owner": true,
    "is_companion": false
  }
}
```

### 3. Register Face Endpoint

```http
POST /api/v1/ai/register-face
Authorization: Bearer {token}
Content-Type: application/json

Request Body:
{
  "ownerId": 333,
  "faceImage": "base64_encoded_image",
  "nationalId": "29801151234567"
}

Response (201):
{
  "success": true,
  "message": "تم تسجيل الوجه بنجاح",
  "faceId": "face_embedding_id"
}
```

---

## 📁 File Storage

### خيارات التخزين

#### 1. Local File System (للتطوير)
```javascript
// Store files locally
const multer = require('multer');
const path = require('path');

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    const uploadPath = path.join(__dirname, 'uploads', file.fieldname);
    cb(null, uploadPath);
  },
  filename: (req, file, cb) => {
    const uniqueName = `${Date.now()}-${file.originalname}`;
    cb(null, uniqueName);
  }
});

const upload = multer({ storage });
```

#### 2. AWS S3 (للإنتاج)
```javascript
// Upload to S3
const AWS = require('aws-sdk');
const s3 = new AWS.S3();

async function uploadToS3(file, type) {
  const key = `${type}/${Date.now()}-${file.originalname}`;
  
  const params = {
    Bucket: process.env.S3_BUCKET,
    Key: key,
    Body: file.buffer,
    ContentType: file.mimetype,
    ACL: 'public-read'
  };
  
  const result = await s3.upload(params).promise();
  return result.Location; // URL
}
```

#### 3. Cloudinary (بديل)
```javascript
// Upload to Cloudinary
const cloudinary = require('cloudinary').v2;

async function uploadToCloudinary(file, type) {
  const result = await cloudinary.uploader.upload(file.path, {
    folder: `ozrix/${type}`,
    resource_type: 'auto'
  });
  
  return result.secure_url;
}
```

---

## 🚀 خطوات التنفيذ

### المرحلة 1: إعداد البنية الأساسية

1. **إنشاء Backend Project**
   ```bash
   # Node.js/Express
   mkdir ozrix-backend
   cd ozrix-backend
   npm init -y
   npm install express mongoose cors dotenv jsonwebtoken bcrypt multer socket.io
   
   # أو Python/Flask
   mkdir ozrix-backend
   cd ozrix-backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install flask flask-cors pymongo flask-jwt-extended bcrypt
   ```

2. **إعداد قاعدة البيانات**
   ```bash
   # Install MongoDB
   # Create database: ozrix_db
   # Create collections: users, vehicles, violations, activities, devices
   ```

3. **إعداد Environment Variables**
   ```env
   # .env
   NODE_ENV=development
   PORT=5000
   MONGODB_URI=mongodb://localhost:27017/ozrix_db
   JWT_SECRET=your_secret_key_here
   JWT_REFRESH_SECRET=your_refresh_secret_here
   S3_BUCKET=ozrix-uploads
   AWS_ACCESS_KEY_ID=your_key
   AWS_SECRET_ACCESS_KEY=your_secret
   ```

### المرحلة 2: تنفيذ Authentication

1. إنشاء User Model
2. إنشاء Auth Routes
3. إنشاء JWT Middleware
4. إنشاء Password Hashing
5. اختبار Login/Logout

### المرحلة 3: تنفيذ Core APIs

1. Violations API
2. Vehicles API
3. Users API
4. Activities API
5. File Upload API

### المرحلة 4: ربط Frontend

1. إنشاء `js/api.js`
2. تحديث `js/pages.js`
3. تحديث `js/auth.js`
4. إزالة Static Data
5. اختبار جميع الصفحات

### المرحلة 5: Real-time Features

1. إعداد WebSocket Server
2. إنشاء `js/realtime.js`
3. تحديث UI للـ Real-time Updates
4. اختبار Real-time Features

### المرحلة 6: ربط Raspberry Pi

1. إنشاء Device Management API
2. إنشاء Device API Keys
3. تحديث Python Code على Raspberry Pi
4. اختبار الاتصال

### المرحلة 7: ربط AI Model

1. إنشاء AI Service
2. إنشاء Face Recognition Endpoints
3. تحديث Raspberry Pi Code
4. اختبار AI Integration

### المرحلة 8: Testing & Deployment

1. Unit Tests
2. Integration Tests
3. Load Testing
4. Security Audit
5. Deployment to Production

---

## 📝 ملاحظات مهمة

### Security

1. **Always hash passwords** - Use bcrypt
2. **Validate all inputs** - Use validation libraries
3. **Sanitize user data** - Prevent XSS attacks
4. **Rate limiting** - Prevent abuse
5. **CORS configuration** - Allow only trusted domains
6. **HTTPS only** - In production

### Performance

1. **Database indexing** - Index frequently queried fields
2. **Caching** - Use Redis for frequently accessed data
3. **Pagination** - Always paginate large datasets
4. **Image optimization** - Compress images before storage
5. **CDN** - Use CDN for static assets

### Error Handling

```javascript
// Standard error response format
{
  "success": false,
  "error": {
    "code": "VIOLATION_NOT_FOUND",
    "message": "المخالفة غير موجودة",
    "details": {}
  }
}
