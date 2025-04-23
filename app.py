from typing import List
from flask import Flask, json, jsonify, make_response, request
from flask_sqlalchemy import SQLAlchemy
from models import db, Terms, Gender, employees, project_tracker, projects,brands,products,orders,order_items
from sqlalchemy import exc
from config import Config
from flask_restx import Api, Resource, reqparse, fields
from datetime import date

#Create an instance of the Flask application
app = Flask(__name__)

config = Config()
app.config.from_object(config)
api = Api(app, version='1.0', title='Your API', description='API Description')
api_ns = api.namespace("Reference", path='/reference', description="Reference Data")
api_fn = api.namespace("Fashion", path='/fashion', description="Fashion Data")
#Initialize the SQLAlchemy extension with the Flask app
db.init_app(app)

with app.app_context():
    db.create_all()

# Define a data model for output marshalling for Project
project_tracker_fields = api.model('project_tracker', {
    'id': fields.Integer,
    'project_number': fields.String(description='The Project name of the project'),
    'title': fields.String(description='The Title name of the project'),
    'description': fields.String(description='The description of the project'),
    'priority': fields.String(description='The priority of the project:1.high 2.medium 3.low'),
    'status': fields.String(description='The status of the project:1.pending 2.in progress 3.completed'),
    'deadline': fields.String(description='The deadline of the project')
})

brands_fields = api.model('brands', {
    'BrandID': fields.Integer,
    'BrandName': fields.String(description='The Project name of the project'),
    'BrandDescription': fields.String(description='The description of the project'),
    'BrandWebsite': fields.String(description='The priority of the project:1.high 2.medium 3.low')
})

orders_fields = api.model('orders', {
    'OrderID': fields.Integer,
    'Customer_ID': fields.String(description='The Project name of the project'),
    'OrderDate': fields.String(description='The description of the project'),
    'TotalAmount': fields.String(description='The priority of the project:1.high 2.medium 3.low'),
    'ShoppingAddress': fields.String(description='The description of the project'),
    'OrderStatus': fields.String(description='The description of the project'),
    'Quantity' : fields.String(description='The description of the project'),
    'Phone' : fields.String(description='The description of the project'),
    'Note' : fields.String(description='The description of the project'),
    'ProductID': fields.Integer,
    'ProductName': fields.String(description='The Project name of the project'),
    'Description': fields.String(description='The description of the project'),
    'Size': fields.String(description='The priority of the project:1.high 2.medium 3.low'),
    'Color': fields.String(description='The description of the project'),
    'Price': fields.String(description='The description of the project'),
    'ImageURL': fields.String(description='The description of the project')

})

products_fields = api.model('products', {
    'ProductID': fields.Integer,
    'ProductName': fields.String(description='The Project name of the project'),
    'Description': fields.String(description='The description of the project'),
    'Size': fields.String(description='The priority of the project:1.high 2.medium 3.low'),
    'Color': fields.String(description='The description of the project'),
    'Price': fields.String(description='The description of the project'),
    'ImageURL': fields.String(description='The description of the project')
})



project_fields = api.model('projects', {
    'employee_id': fields.Integer,
    'project_number': fields.String(description='The Project name of the project'),
})

employee_fields = api.model('employees', {
    'employee_id': fields.Integer,
    'last_name': fields.String(description='The last name of employee'),
    'first_name': fields.String(description='The first name of employee')
})
    
# Define a data model for input
put_projects_parser = reqparse.RequestParser()
put_projects_parser.add_argument('project_number', type=str, required=True)
put_projects_parser.add_argument('title', type=str, required=True)
put_projects_parser.add_argument('description', type=str, required=True)
put_projects_parser.add_argument('priority', type=int, required=True)
put_projects_parser.add_argument('status', type=int, required=True)
put_projects_parser.add_argument('deadline', type=str, required=True)

put_orders_parser = reqparse.RequestParser()
put_orders_parser.add_argument('customerId',type=str,required=True)
put_orders_parser.add_argument('productId',type=int,required=True)
put_orders_parser.add_argument('quantity',type=int,required=True)
put_orders_parser.add_argument('itemprice',type=float,required=True)
put_orders_parser.add_argument('address',type=str,required=True)
put_orders_parser.add_argument('phone',type=str,required=True)
put_orders_parser.add_argument('note',type=str,required=True)

put_orders_lst_parser = reqparse.RequestParser()
put_orders_lst_parser.add_argument('customerId',type=str,required=True)
 
@api_fn.route('/brands')
class CVLProjects(Resource):
    @api.marshal_with(brands_fields)
    def get(self):
            trackers = db.session.query(brands).all()
            lst=[v for v in trackers]
            return lst
        
@api_fn.route('/products')
class CVLProjects(Resource):
    @api.marshal_with(products_fields)
    def get(self):
            trackers = db.session.query(products).all()
            lst=[v for v in trackers]
            return lst

@api_fn.route('/orders')
class CVLProjects(Resource):
    @api.marshal_with(orders_fields)
    @api.expect(put_orders_lst_parser)
    def get(self):
            argsl = put_orders_lst_parser.parse_args()
            trackers = db.session.query(
    orders.OrderID,
    orders.Customer_ID,
    orders.OrderDate,
    orders.TotalAmount,
    orders.ShoppingAddress,
    orders.OrderStatus,
    orders.Quantity,
    orders.Phone,
    orders.Note,
    products.ImageURL,
    products.ProductName,
    products.Size,
    products.Price,
    products.Color,
    products.Description,
    products.ProductID
).join(products, orders.ProductID == products.ProductID) \
 .filter(orders.Customer_ID == argsl["customerId"]).all()
            lst=[v for v in trackers]
            return lst
    @api.expect(put_orders_parser)
    def post(self): 
        try:
            args = put_orders_parser.parse_args()
            datetime_object =  date.today()
            totalamt = args["quantity"] * args["itemprice"]
            t = orders(Customer_ID = args["customerId"], 
                OrderDate = datetime_object,
                TotalAmount = totalamt, 
                ShoppingAddress = args["address"],
                OrderStatus = "Ordered",
                ProductID = args["productId"],
                Quantity=args["quantity"] ,
                Phone=args["phone"],
                Note=args["note"])
            db.session.add(t)
            db.session.commit()
            return {'message':'success'}, 201
        except Exception as e:
                print (e)
                return {'message': 'Something went wrong!'}, 500
           
@api_ns.route('/projects')
class CVLProjects(Resource):
    @api.marshal_with(project_tracker_fields)
    def get(self):
            trackers = db.session.query(project_tracker).all()
            for tracker in trackers:
                if tracker.priority==1: tracker.priority='high'
                elif tracker.priority==2: tracker.priority='medium'
                else: tracker.priority='low'
                if tracker.status==1: tracker.status='pending'
                elif tracker.status==2: tracker.status='in progress'
                else: tracker.status='completed'
            lst=[v for v in trackers]
            return lst
    @api.expect(put_projects_parser)
    def post(self): 
        try:
            args = put_projects_parser.parse_args()
            tracker = db.session.query(project_tracker).filter_by(project_number=args["project_number"]).first()
            if tracker:
                return {'message':'This project number is existed'}, 201
            else:
                datetime_object = datetime.strptime(args["deadline"], '%Y-%m-%d').date()
                t = project_tracker(project_number = args["project_number"], 
                    title = args["title"],
                    deadline = datetime_object,
                    description = args["description"], 
                    priority = args["priority"],
                    status = args["status"])
                db.session.add(t)
                db.session.commit()
                return {'message':'success'}, 201
        except Exception as e:
                print (e)
                return {'message': 'Something went wrong!'}, 500

@api_ns.route('/projects/<string:project_number>')
class GetProjectTrackerResource(Resource):
    @api.marshal_with(project_tracker_fields)
    def get(self, project_number):
        tracker = db.session.query(project_tracker).filter_by(project_number=project_number).first()
        if tracker:
            if tracker.priority==1: tracker.priority='high'
            elif tracker.priority==2: tracker.priority='medium'
            else: tracker.priority='low'
            if tracker.status==1: tracker.status='pending'
            elif tracker.status==2: tracker.status='in progress'
            else: tracker.status='completed'
            return tracker
        return {'message': 'Project tracker not found'}, 404
    
@api_ns.route('/projects/<int:id>')
class GetProjectTrackerResource(Resource):  
    @api.marshal_with(project_tracker_fields)
    def get(self, id):
        tracker = db.session.query(project_tracker).filter_by(id=id).first()
        if tracker:
            if tracker.priority==1: tracker.priority='high'
            elif tracker.priority==2: tracker.priority='medium'
            else: tracker.priority='low'
            if tracker.status==1: tracker.status='pending'
            elif tracker.status==2: tracker.status='in progress'
            else: tracker.status='completed'
            return tracker
        return {'message': 'Project tracker not found'}, 404
    
    @api.response(204, 'This record deleted successfully')
    def delete(self, id):
        tracker = db.session.query(project_tracker).filter_by(id=id).first()
        if tracker:
            db.session.delete(tracker)
            db.session.commit()
            return '', 204
        else:
            return {'message': 'Project Tracker not found'}, 404
    
    @api.expect(put_projects_parser)
    def put(self, id):
        tracker = db.session.query(project_tracker).filter_by(id=id).first()
        if tracker:
            try:
                args = put_projects_parser.parse_args()
                datetime_object = datetime.strptime(args["deadline"], '%Y-%m-%d').date()
                tracker.project_number=args["project_number"]
                tracker.title=args["title"]
                tracker.description=args["description"]
                tracker.priority=args["priority"]
                tracker.status=args["status"]
                tracker.deadline=datetime_object
                db.session.commit()
                return {'message':'This record is updated successfully'}, 201
            except Exception as e:
                    print (e)
                    return {'message': 'Something went wrong!'}, 500
        else:
            return {'message': 'Project Tracker not found'}, 404
        
@api_ns.route('/project/<string:project_number>')
class GetProjectInfoResource(Resource): 
    @api.marshal_with(employee_fields) 
    def get(self, project_number):
        info = db.session.query(projects).filter_by(project_number=project_number).all()
        if info:
            lst=[]
            for i in info:
                lst+= db.session.query(employees).filter_by(employee_id=i.employee_id).all()
        return lst
        #lst=[e for e in emp1]
        #return lst
            #else:    
            #return {'message': 'Project info not found'}, 404
    
@api.route('/swagger')
class SwaggerResource(Resource):
    def get(self):
        return api.swagger_ui()

#Run the Flask app
if __name__=='__main__':
    app.run(host="0.0.0.0", port=10000)