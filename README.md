
# Mastering Amazon S3 Bucket Configuration and Access Control
This assignment shows the  process of setting up and managing an Amazon S3 bucket. 

Tasks:

## 1. Creating an Amazon S3 Bucket:

### Steps
1. Set the region to `us-west-2` 
2. Click the Create bucket button on the console.
3. Keep settings default
4. Choose a unique name `week7skillsyncbucket`
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/week7skillsyncbucket.png)
### Challenges
I did not experience any challenges
### Outcomes
An S3 bucket with the name `week7skillsyncbucket`
 
## 2. Upload a Sample File:

### Steps
1. Click on the `week7skillsyncbucket`
2. Click `Upload` to open upload widget
3. Click `Add files` to open file explorer. Select a file then click `Open`
4. Once file is loaded, Click `Upload` to upload the file
5. Click on the uploaded file to reveal its properties
6. Copy the Object URL to a new tab then observe 
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/uploadedobject.png)
### Challenges
I did not experience any challenges
### Outcomes
The file will be uploaded successfully. However, when trying to access the file via the Object URL, I get an error
message.
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/errormessage.png) 

3. Apply a Bucket Policy:

### Steps
1. Navigate to IAM > Users > Chan
2. Click on `Add Permissions`
3. Select `Attach policies directly` 
4. Search for `AmazonS3ReadOnly` in the Permissions policies and select it. Click `Next`
5. Click `Add Permissions` to grant read-only access to Chan.
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/s3readonlyaccess.png)
### Challenges
I did not experience any challenges
### Outcomes
User Chan can only view the object inside the S3 bucket. But when Chan attempts to either upload or delete the object, he gets the error message, `Access Denied`.
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/s3bucketpolicyuploadfail.png)  

4. Set Up IAM Permissions:

### Steps
1. Navigate to IAM > Policies > Create policy
2. Choose S3 Service
3. Search `putobject` and select
4. Specify ARN by clicking Add ARNs. Fill in the required details
5. Provide policy details, review then create policy 
6. Navigate to IAM > User groups
7. Create group
8. Provie the User Group name
9. Add user Chan to the group. Attach the `S3Uploadfiles` policy to the IAM Group. Create user group
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/iamusergroup.png)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/putbojectpolicyrole.PNG)

### Challenges
I did not experience any challenge

### Outcomes
User Chan could upload a file to the bucket.
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/fileuploadsuccess.png)

5. Assign an IAM Role to EC2:

### Steps
1. Navigate to IAM > Roles
2. Create role
3. Select AWS service as Trusted Entity Type
4. Choose S3 as the Use case
5. Add `AmazonS3FullAccess`then Next
6. Provide role name and description then create role
7. Launch an EC2 instance then attach `EC2S3FullAccess` instance role to the EC2 Instance
8. Once EC2 instance is running, Connect to the instance to access the terminal
9. Type `aws s3 cp wget-log s3://week7skillsyncbucket` to test file upload to S3 from the EC2 instance
10. Confirmed that the file was uploaded using the command `aws s3 ls s3://week7skillsyncbucket --recursive`
### Challenges
I experienced problems at first, trying to connect the EC2 instance until I found out that I had launched the instance in a private subnet. So i had to terminate and recreate the instance in a public subnet and also enabled the auto-assign Public IP as that too, was preventing me from accessing the ec2 instance via SSH. 
### Outcomes
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/iamroleattached.png)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/uploadedwgetlogviaec2.png)
6. Enable Versioning:

### Steps
1. Open EC2 terminal
2. Type in the command `aws s3api put-bucket-versioning --bucket week7skillsyncbucket --versioning-configuration Status=Enabled
3. Navigate to S3 Bucket properties page to confirm Versioning status
4. Upload wget-log multiple times and make changes to it, for each attempt
5. Delete the original wget-log file
6. Toggle the `show versions` button to reveal the version trail of the wget-log file
### Challenges
I did not experience any challenges
### Outcome
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/s3versioningenabled.png)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/objectversionsuploaded.png)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/bucketversioningenabled.png)

7. Configure Logging:

### Steps
1. Navigate to Amazon S3> Buckets> week7skillsyncbucket
2. Edit Server access logging
3. Enable server access logging
4. Choose secondary bucket `Week7bucketklogs`
5. select the log object key format
6. Save changes
### Challenges
I did not experience any challenges
### Outcome
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/loggingconfiguration.png)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/week7skillsynclogscaptured.PNG)

8. Integrate S3 with an Application:

### Steps
1. Access VSCode 
2. Opened Debian terminal from VSCode to download Python3 using the following commands:
```
#!/bin/bash

# Update the package list
sudo apt update

# Install Python3 and pip if not installed
sudo apt install -y python3 python3-pip python3-tk

# Install boto3 using pip
sudo apt install python3.boto3

```
3. Configured my AWS CLI with my AWS credentials
`aws configure`
4. Create file s3uploadergui.py to host the python script below:
```
import tkinter as tk
from tkinter import filedialog, messagebox
import boto3
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

class S3UploaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("S3 Uploader")
        
        # Configure layout
        self.label = tk.Label(root, text="Select a file to upload:")
        self.label.pack(pady=10)
        
        self.upload_button = tk.Button(root, text="Browse", command=self.browse_file)
        self.upload_button.pack(pady=5)
        
        self.upload_button = tk.Button(root, text="Upload to S3", command=self.upload_file)
        self.upload_button.pack(pady=5)
        
        self.file_path = None
        self.bucket_name = "week7skillsyncbucket"  # Replace with your bucket name

    def browse_file(self):
        self.file_path = filedialog.askopenfilename()
        if self.file_path:
            messagebox.showinfo("File Selected", f"Selected file: {self.file_path}")

    def upload_file(self):
        if not self.file_path:
            messagebox.showerror("Error", "No file selected.")
            return

        s3_client = boto3.client('s3')
        try:
            s3_client.upload_file(self.file_path, self.bucket_name, self.file_path.split('/')[-1])
            messagebox.showinfo("Success", f"File {self.file_path} uploaded successfully!")
        except FileNotFoundError:
            messagebox.showerror("Error", "The file was not found.")
        except NoCredentialsError:
            messagebox.showerror("Error", "Credentials not available.")
        except PartialCredentialsError:
            messagebox.showerror("Error", "Incomplete credentials provided.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = S3UploaderApp(root)
    root.mainloop()
```
5. Configure CORS for `week7skillsyncbucket` by using the AWS CLI command below:
` aws s3api put-bucket-cors --bucket week7skillsyncbucket --cors-configuration '{"CORSRules" : [{"AllowedHeaders":["Authorization"],"AllowedMethods":["GET","HEAD"],"AllowedOrigins":["*"],"ExposeHeaders":["Access-Control-Allow-Origin"]}]}'`
6. Added the following bucket policy below to allow uploads via the Bucket policy section under Amazon S3 > Bucket > week7skillsyncbucket
```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": "*",
            "Action": [
                "s3:PutObject",
                "s3:GetObject"
            ],
            "Resource": "arn:aws:s3:::week7skillsyncbucket/*"
        }
    ]
}
```
7. I then ran the application by executing the following script in the terminal:
`python3 s3uploadergui.py`
8. The GUI popped up and I interacted with the GUI, using Browse and Upload functionality. 

### Challenges
I encountered a challenge when I first executed the script to launch the GUI application. I realized that I had to specify the python version i.e. python3 to execute the application. Also, tkinter was missing in the initial install of Python so I had to execute the reinstall tkinter using the command `sudo apt-install python3-tk`
### Outcome
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/pythons3uploaderapplication.PNG)
![Snapshot](https://github.com/slimfeet/Week7S3Task/blob/main/fileuploadedviapp.PNG)
