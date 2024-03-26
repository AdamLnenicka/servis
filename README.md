

This project involved designing use cases, wireframes, and a database model, followed by implementing HTML templates, CSS styles, and a SQLite3 database. The web application, built using Python and Flask, includes features such as registration, login, user profile management, and role-based functionalities. Security and functionality testing were conducted using various user roles. The application routes handle specific tasks like registration, login, user profiles, order management, and vehicle status display. The functions.py file manages database operations for user management, vehicle handling, and technical record processing.

Detailed project information can be found at .docx documentation.

<h2>Functionality of the application:</h2>

1. User management:
   - Administrator: Has full access to all application functions, including user management, roles, and permissions.
   - Department managers: Have access to relevant departments (technical inspection, service, disposal) and can manage records, plans, and resources assigned to these departments.
   - Technicians: Can record the results of technical inspections and performed service work, only for vehicles assigned to them.
   - Customers: Can monitor the status of their vehicles, schedule technical inspection and service appointments.
2. Vehicle management:
   - Ability to add, modify, and delete vehicle records.
   - Tracking the history of technical inspections, services, and disposal for each vehicle.
3. Planning and calendar:
   - Scheduling technical inspection and service appointments.
   - Calendar overview with filtering options by department, technicians, and vehicles.
4. Status monitoring:
   - Monitoring the current status of technical inspections and service work.
   - Notifications for technicians, managers, and customers regarding upcoming appointments and completed tasks (displayed upon login in the application, no need for push notifications).
5. Messages and statistics:
   - Generating reports and statistics related to technical inspections, services, and disposal.
   - Creating clear visualizations for managers.

<h2>Permissions and roles:</h2>

1. Administrator / boss

2. Technical inspection manager

3. Service manager

4. Scrap disposal manager

5. Technical inspection technician

6. Service technician

7. Scrap disposal technician

8. Customer

<h2>Technical requirements:</h2>

- The application will be developed as a web application with responsive design to be usable on various devices.

- A modern web framework with a database system for data storage will be used for application development.

- Security measures will include user authentication, role verification, and input data control.

<h2>Additional requirements:</h2>

- The application will be intuitive and easy to use for users of different technical levels.

- It will be ensured that different user roles will have access only to functions and data relevant to their work.

- The application will support multi-language localization to be usable in different regions.

Expected output: A fully functional web application with a user interface and backend logic that enables efficient management of vehicle technical inspections, services, and scrap disposal, with a focus on various user roles and their permissions.


![image](https://github.com/AdamLnenicka/servis/assets/70570107/1d58ab7b-de12-48ec-be6e-621b4a4d5de9)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/037ec023-08bc-4fdf-8cee-b37659551855)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/d5380dd1-db5f-49c2-9af1-15eedabaebbb)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/961f869f-2cc2-4ce8-97ec-be0428c84bfe)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/cd105f6e-6fba-4730-9666-3546e4c723c6)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/0fef05a2-f47c-4545-bdb3-ea9521f194e9)

![image](https://github.com/AdamLnenicka/servis/assets/70570107/ebd9e24e-7402-49cc-b883-290d3563486e)


