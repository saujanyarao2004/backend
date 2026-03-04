from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from database import Base


# ==========================================================
# USERS TABLE
# ==========================================================
class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    email = Column(String(150), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(String(20), nullable=False)  # patient / doctor / admin
    is_active = Column(Boolean, default=True)
    created_at = Column(TIMESTAMP, server_default=func.now())

    audit_logs = relationship("AuditLog", back_populates="user")


# ==========================================================
# PATIENTS TABLE
# ==========================================================
class Patient(Base):
    __tablename__ = "patients"

    patient_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    gender = Column(String(10))
    contact_number = Column(String(20))
    address = Column(String)
    created_at = Column(TIMESTAMP, server_default=func.now())


# ==========================================================
# DOCTORS TABLE
# ==========================================================
class Doctor(Base):
    __tablename__ = "doctors"

    doctor_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    first_name = Column(String(100))
    last_name = Column(String(100))
    specialization = Column(String(150))
    license_number = Column(String(100))
    hospital_name = Column(String(150))
    age = Column(Integer)
    years_of_experience = Column(Integer)

    created_at = Column(TIMESTAMP, server_default=func.now())


# ==========================================================
# CONSENTS TABLE
# ==========================================================
class Consent(Base):
    __tablename__ = "consents"

    consent_id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)

    status = Column(String(20), default="PENDING")

    otp_code = Column(String(10))
    otp_expires_at = Column(TIMESTAMP)

    granted_at = Column(TIMESTAMP)
    revoked_at = Column(TIMESTAMP)


# ==========================================================
# AUDIT LOGS TABLE
# ==========================================================
class AuditLog(Base):
    __tablename__ = "audit_logs"

    log_id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)

    action = Column(String(50), nullable=False)
    entity_type = Column(String(50), nullable=False)
    entity_id = Column(Integer, nullable=False)

    created_at = Column(TIMESTAMP, server_default=func.now())

    user = relationship("User", back_populates="audit_logs")

# ==========================================================
# MEDICAL RECORDS TABLE
# ==========================================================
class MedicalRecord(Base):
    __tablename__ = "medical_records"

    record_id = Column(Integer, primary_key=True, index=True)

    patient_id = Column(Integer, ForeignKey("patients.patient_id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.doctor_id"), nullable=False)

    diagnosis = Column(String)
    treatment = Column(String)
    prescription = Column(String)

    created_at = Column(TIMESTAMP, server_default=func.now())

    # relationships
    files = relationship("MedicalFile", back_populates="record")


# ==========================================================
# MEDICAL FILES TABLE
# ==========================================================
class MedicalFile(Base):
    __tablename__ = "medical_files"

    file_id = Column(Integer, primary_key=True, index=True)

    record_id = Column(Integer, ForeignKey("medical_records.record_id"), nullable=False)

    file_name = Column(String(255))
    file_url = Column(String(500))
    file_type = Column(String(50))

    uploaded_at = Column(TIMESTAMP, server_default=func.now())

    # relationship
    record = relationship("MedicalRecord", back_populates="files")    