from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from datetime import datetime
from sqlalchemy import desc


# basic layout
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "" #Your DB Settings
db = SQLAlchemy(app)
migrate = Migrate(app,db)


class Employee(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  firstname = db.Column(db.String(80), unique=False, nullable=False)
  lastname = db.Column(db.String(80), unique=False, nullable=False)
  dob = db.Column(db.DateTime, unique=False, nullable=False)
  vehicle = db.relationship("Vehicle", backref="employee", lazy=True)

  def getFirstName(self):
    return self.firstname

  def getLastName(self):
    return self.lastname

  def getDob(self):
    return self.dob.date()

  def getId(self):
    return self.id


class Vehicle(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), unique=False, nullable=False)
  year = db.Column(db.DateTime, unique=False, nullable=False)
  employeeId = db.Column(db.Integer, db.ForeignKey("employee.id"))

  def getId(self):
    return self.id

  def getYear(self):
    return self.year.year #Only Shows Year

  def getName(self):
    return self.name

  def getEmployeeId(self):
    return self.employeeId


def convertDate(string):
  datetime_object = datetime.strptime(string, "%Y-%m-%d")
  return datetime_object
  

if __name__ == "__main__":
  with app.app_context():
    upgrade()


  while True:
    print()
    print("1. Create new Employee")
    print("2. Show all Employees")
    print("3. Buy New Vehicle to employee (not car from fleet)")
    print("4. Show Specific Employee Vehicles")
    print("5. Change Car Name")
    print("6. Show all cars that the company owns")
    print("7. Add Car To Fleet")
    print("8. Show Cars And Its Current Owner")
    print("9. Assign A Car In The Fleet To An Employee")
    sel = input("Enter: ")

    if sel == "1":
      emp = Employee()
      emp.firstname = input("Enter First Name: ").capitalize()
      emp.lastname = input("Enter Lastname: ").capitalize()
      dob = input("Enter DoB, YYYY-MM-DD: ")
      emp.dob = convertDate(dob)

      db.session.add(emp)
      db.session.commit()
    
    if sel == "2":
      for employee in Employee.query.all():
        print(f"{employee.getFirstName()} {employee.getLastName()} - {employee.getDob()}\n")
      
    if sel == "3":
      getNamn = input("Enter Name Employee: ").capitalize()
      some_employee = Employee.query.filter_by(firstname=getNamn).first()
      addVehicle = Vehicle()
      addVehicle.name = input("What Car Brand: ").title()
      year = input("Enter Car Year YYYY-MM-DD: ")
      addVehicle.year = convertDate(year)
      some_employee.vehicle.append(addVehicle)
      db.session.commit()

    if sel == "4":
      getNamn = input("Enter Name Employee: ").capitalize()
      some_employee = Employee.query.filter_by(firstname=getNamn).first()
      if not some_employee:
        print("That employee doesnt exist in db")
        continue
      for vehicle in some_employee.vehicle:
        print(f"This Employee Drives:\n{vehicle.getName()} - {vehicle.getYear()}")


    if sel == "5":
      for vehicle in Vehicle.query.all():
        print(f"{vehicle.getId()}, {vehicle.getName()} - {vehicle.getYear()}\n")
      sel = int(input("Enter ID of the car in question: "))
      updateCar = Vehicle.query.filter_by(id=sel).first()
      updateCar.name = input("Enter new car name: ").title()
      print(f"Car name updated to {updateCar.name}..")
      db.session.commit()

    if sel == "6":
      for vehicle in Vehicle.query.all():
        print(f"{vehicle.getName()} - {vehicle.getYear()}\n")

    if sel == "7":
      car = Vehicle()
      car.name = input("Enter Car Name: ").title()
      year = input("Enter Car Year YYYY-MM-DD: ")
      car.year = convertDate(year) # converting String --> DateTime object
      db.session.add(car)
      db.session.commit()

    #Måste joina employee och Vehicles och order by desc == lista
    #Fuck Yes, denna var svår
    if sel == "8":
      result = db.session.query(Employee, Vehicle).join(Vehicle).filter(Vehicle.employeeId==Employee.id).order_by(desc(Vehicle.name)).all()
      for employee, vehicle in result:
        print(f"{employee.getFirstName()} {employee.getLastName()} - {vehicle.getName()}, {vehicle.getYear()}\n")

    
    if sel == "9":
      for vehicle in Vehicle.query.all():
        if vehicle.getEmployeeId() != None: # Så vi bara får dem som inte är använda
          print("\nNo vehicles available")
          break
        else:
          print(f"{vehicle.getId()}, {vehicle.getName()} - {vehicle.getYear()}\n")
          getCarId = int(input("Enter ID of the car in question: "))

          for employee in Employee.query.all():
            print(f"{employee.getId()}, {employee.getFirstName()} {employee.getLastName()}")
          
          getEmployeeId = int(input("Which Employee?: "))
          
          some_car = Vehicle.query.filter_by(id=getCarId).first()
          some_car.employeeId = getEmployeeId
          db.session.commit()
      
