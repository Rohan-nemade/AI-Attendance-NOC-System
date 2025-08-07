from sqlalchemy import Column,Integer,String,Boolean,ForeignKey,DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

class student(Base):
    __tablename__ = "students"

    id = Column(Integer,primary_key=True,index = True)
    name = Column(String,index = True)
    roll_number = Column(String,unique=True,index=True)

    assignments = relationship("Assignment", back_populates="student")
    mark = relationship("TeacherMark",back_populates="student")

class Assignment(Base):
    __tablename__ = "assignments"

    id = Column(Integer,primary_key=True,index=True)
    student_id = Column(Integer,ForeignKey("students.id"))
    subject = Column(String)
    file_path = Column(String)
    uploaded_at = Column(String,default=datetime.now)
    similarity_score = Column(String,default=None)

    student = relationship("Student", back_populates="assignments")

class TeacherMark(Base):
    __tablename__ = "teacher_marks"

    id = Column(Integer,primary_key=True,index=True)
    student_id = Column(Integer, ForeignKey("students.id"))
    subjects = Column(String)

    sce = Column(Integer,default = False)
    cie = Column(Boolean,default = False)
    ha = Column(Boolean,default = False)

    student = relationship("Student",back_populates="marks")
