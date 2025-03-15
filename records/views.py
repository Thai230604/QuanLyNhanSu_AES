import os
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from .models import *
import base64
import json
from django.core.exceptions import ObjectDoesNotExist

def home(request):
    return render(request, 'records/base.html')

def validate_key(encryption_key):
    """Kiểm tra khóa mã hóa hợp lệ."""
    if not encryption_key or len(encryption_key) != 16:
        return False, "Khóa mã hóa phải có đúng 16 ký tự."
    return True, None


def aes_encrypt(key, data):
    key_bytes = key.encode('utf-8')  
    iv = os.urandom(16)  
    cipher = AES.new(key_bytes, AES.MODE_CFB, iv)
    encrypted_data = iv + cipher.encrypt(data) 
    return encrypted_data



def handle_encrypt_file(file, encrypted_data):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    encrypted_filename = os.path.join(downloads_path, file.name + '.enc')
    with open(encrypted_filename, 'wb') as enc_file:
        enc_file.write(encrypted_data)
    return encrypted_filename


def encrypt(request):
    if request.method == 'POST':
        encryption_key = request.POST.get('encryption_key')
        uploaded_file = request.FILES.get('file')

        # Kiểm tra khóa hợp lệ
        is_valid, error_message = validate_key(encryption_key)
        if not is_valid:
            messages.error(request, "Khóa mã hóa phải có đúng 16 ký tự.")
            return render(request, 'records/encrypt.html')

        if not uploaded_file:
            messages.error(request, "Vui lòng tải lên tệp để mã hóa.")
            return render(request, 'records/encrypt.html')

        # Đọc nội dung file
        file_data = uploaded_file.read()

        # Mã hóa dữ liệu
        encrypted_data = aes_encrypt(encryption_key, file_data)

        # Lưu file mã hóa
        encrypted_filename = handle_encrypt_file(uploaded_file, encrypted_data)

        messages.success(request, f"Tệp đã được mã hóa thành công! Lưu với tên: {encrypted_filename}")
        return render(request, 'records/encrypt.html')

    return render(request, 'records/encrypt.html')

def aes_decrypt(key, encrypted_data):
    key_bytes = key.encode('utf-8')  # Chuyển đổi khóa sang bytes
    iv = encrypted_data[:16]  # Lấy Initialization Vector (IV) từ 16 byte đầu tiên
    cipher = AES.new(key_bytes, AES.MODE_CFB, iv)
    decrypted_data = cipher.decrypt(encrypted_data[16:])  # Giải mã phần dữ liệu còn lại
    return decrypted_data




def handle_decrypted_file(file_data, new_filename):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    new_file_path = os.path.join(downloads_path, new_filename)
    with open(new_file_path, 'wb') as dec_file:
        dec_file.write(file_data)
    
    return new_file_path

def decrypt(request):
    if request.method == 'POST':
        decryption_key = request.POST.get('decryption_key')
        uploaded_file = request.FILES.get('file')
        new_file_name = request.POST.get('new_file_name')

        # Kiểm tra khóa hợp lệ
        is_valid, error_message = validate_key(decryption_key)
        if not is_valid:
            messages.error(request, error_message)
            return redirect('decrypt')  # Redirect lại để hiển thị thông báo lỗi

        if not uploaded_file:
            messages.error(request, "Vui lòng tải lên tệp mã hóa.")
            return redirect('decrypt')  # Redirect lại để hiển thị thông báo lỗi

        if not new_file_name:
            messages.error(request, "Vui lòng nhập tên file mới.")
            return redirect('decrypt')  # Redirect lại để hiển thị thông báo lỗi

        # Đọc nội dung file đã mã hóa
        encrypted_data = uploaded_file.read()

        try:
            decrypted_data = aes_decrypt(decryption_key, encrypted_data)

            saved_filename = handle_decrypted_file(decrypted_data, new_file_name)

            messages.success(request, f"Tệp đã được giải mã! Lưu với tên: {saved_filename}")
            return redirect('decrypt')  # Redirect lại để hiển thị thông báo thành công
        except Exception as e:
            messages.error(request, f"Đã xảy ra lỗi khi giải mã: {str(e)}")
            return redirect('decrypt')  # Redirect lại để hiển thị thông báo lỗi

    return render(request, 'records/decrypt.html')



#  ---------------------------------------------------------------------------Nhaan su----------------------------------------------------------

def encrypt_aes(data, key):
    data = pad(data.encode('utf-8'), 16)  # Padding tự động
    iv = get_random_bytes(16)  # Tạo IV ngẫu nhiên
    cipher = AES.new(key, AES.MODE_CBC, iv)  # Tạo cipher
    encrypted_data = cipher.encrypt(data)  # Mã hóa
    return base64.b64encode(iv + encrypted_data).decode('utf-8')  # Trả về kết quả

def handle_file_upload(employee_id, key_data):
    downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
    file_path = os.path.join(downloads_path, f"{employee_id}_key.json")
    with open(file_path, 'w') as file:
        file.write(key_data)
    return file_path


def add(request):
    departments = Department.objects.all()  # Lấy danh sách phòng ban
    if request.method == 'POST':
        try:
            id = request.POST.get('employee_code')
            name = request.POST.get('name') or "N/A"
            birth_date = request.POST.get('birth_date') or "0000-00-00"
            address = request.POST.get('address') or "N/A"
            phone_number = request.POST.get('phone_number') or "0000000000"
            position = request.POST.get('position') or "Unknown"
            department_id = request.POST.get('department')  # Nhận giá trị khóa ngoại

            # Tạo khóa ngẫu nhiên
            random_key = get_random_bytes(16)
            key_base64 = base64.b64encode(random_key).decode('utf-8')

            # Mã hóa dữ liệu
            encrypted_name = encrypt_aes(name, random_key)
            encrypted_date = encrypt_aes(birth_date, random_key)
            encrypted_address = encrypt_aes(address, random_key)
            encrypted_phone = encrypt_aes(phone_number, random_key)
            encrypted_position = encrypt_aes(position, random_key)

            # Lấy đối tượng phòng ban từ ID
            department = None
            if department_id:
                try:
                    department = Department.objects.get(id=department_id)
                except Department.DoesNotExist:
                    messages.error(request, "Phòng ban không tồn tại.")
                    return render(request, 'records/add.html', {'departments': departments})
            else:
                messages.error(request, "Nhập đầy đủ thông tin")
                return render(request, 'records/add.html', {'departments': departments})

            # Lưu vào database
            employee = Employee(
                employee_code=id,
                name=encrypted_name,
                birth_date=encrypted_date,
                address=encrypted_address,
                phone_number=encrypted_phone,
                position=encrypted_position,
                department=department
            )
            employee.save()

            # Lưu file chứa khóa mã hóa
            file_content = {
                "employee_code": id,
                "encryption_key": key_base64
            }
            key_data = json.dumps(file_content, indent=4)
            file_path = handle_file_upload(id, key_data)

            # Hiển thị thông báo
            messages.success(request, f"Thêm nhân viên thành công! Khóa mã hóa đã được lưu vào: {file_path}")
        except:
            messages.error(request, "Mã nhân viên đã tồn tại")

    # Truyền danh sách phòng ban và thông báo nếu có
    return render(request, 'records/add.html', {'departments': departments})

   
    

def employee_list(request, department_id):
    department = get_object_or_404(Department, id=department_id)
    employees = Employee.objects.filter(department=department)

    context = {
        'department': department,
        'employees': employees,
    }
    return render(request, 'records/employee_list.html', context)


def decrypt_aes(encrypted_data, key):
    
    encrypted_data = base64.b64decode(encrypted_data)

    iv = encrypted_data[:16]

    cipher_data = encrypted_data[16:]

    cipher = AES.new(key, AES.MODE_CBC, iv)

    decrypted_data = cipher.decrypt(cipher_data)

    decrypted_data = unpad(decrypted_data, AES.block_size)

    return decrypted_data.decode('utf-8')



def delete_employee(request, employee_id):
    if request.method == 'POST':

        employee = get_object_or_404(Employee, id=employee_id)
        
        department_id = employee.department.id if employee.department else None
        downloads_path = os.path.join(os.path.expanduser("~"), "Downloads")
        
        file_path = os.path.join(downloads_path, f"{employee.employee_code}_key.json")
        
        try:
            employee.delete()

            if os.path.exists(file_path):
                os.remove(file_path)
                messages.success(request, f"File {file_path} đã được xóa.")
            
            messages.success(request, "Nhân viên đã được xóa thành công.")
        except Exception as e:
            messages.error(request, f"Lỗi khi xóa nhân viên: {str(e)}")

    # Chuyển hướng về trang danh sách nhân viên của phòng ban sau khi xóa
    return redirect('employee_list', department_id=department_id)

def employee_decrypt(request, department_id):
    if request.method == 'POST':
        # Lấy id nhân viên và file khóa
        employee_id = request.POST.get('employee_id')
        key_file = request.FILES.get('key_file')

        if key_file:
            key_data = key_file.read().decode('utf-8')
            key_json = json.loads(key_data)
            key_base64 = key_json.get('encryption_key')
            file_employee_id = key_json.get('employee_code')

            if not key_base64:
                messages.error(request, "Khóa giải mã không hợp lệ.")
                return redirect('employee_list', department_id=department_id)
            
            # Giải mã khóa
            key = base64.b64decode(key_base64)

            try:
                # Lấy thông tin nhân viên
                employee = Employee.objects.get(id=employee_id)

                if employee.employee_code != file_employee_id:
                    messages.error(request, "Khóa giải mã không hợp lệ.")
                    return redirect('employee_list', department_id=department_id)

                # Giải mã dữ liệu
                decrypted_name = decrypt_aes(employee.name, key)
                decrypted_date = decrypt_aes(employee.birth_date, key)
                decrypted_address = decrypt_aes(employee.address, key)
                decrypted_phone = decrypt_aes(employee.phone_number, key)
                decrypted_position = decrypt_aes(employee.position, key)

                # Truyền dữ liệu vào template employee_decrypt.html
                return render(request, 'records/employee_decrypt.html', {
                    'employee': employee,
                    'decrypted_name': decrypted_name,
                    'decrypted_birth_date': decrypted_date,
                    'decrypted_address': decrypted_address,
                    'decrypted_phone_number': decrypted_phone,
                    'decrypted_position': decrypted_position,
                    'department_id': department_id,
                })

            except ObjectDoesNotExist:
                messages.error(request, "Không tìm thấy nhân viên.")
                return redirect('employee_list', department_id=department_id)
            except ValueError as e:
                if "padding" in str(e).lower():
                    messages.error(request, "Lỗi giải mã: Khóa hoặc dữ liệu không hợp lệ.")
                else:
                    messages.error(request, f"Lỗi giải mã: {str(e)}")
                return redirect('employee_list', department_id=department_id)
        else:
            messages.error(request, "Không có file khóa.")
            return redirect('employee_list', department_id=department_id)

    return redirect('employee_list', department_id=department_id)

def update_employee(request, employee_id):
    employee = get_object_or_404(Employee, id=employee_id)

    if request.method == 'POST':
        # Get new employee data
        name = request.POST.get('name')
        birth_date = request.POST.get('birth_date')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        position = request.POST.get('position')

        # Process the decryption key file upload
        key_file = request.FILES['key_file']
        key_data = json.load(key_file)

        decryption_key = base64.b64decode(key_data['encryption_key'])
        id = key_data['employee_code']
        
        if id != employee.employee_code:
            messages.error(request, "Lỗi mã hóa: Khóa hoặc dữ liệu không hợp lệ.")
            return redirect('employee_list', department_id=employee.department_id)
            

        encrypted_name = encrypt_aes(name, decryption_key)
        encrypted_birth_date = encrypt_aes(birth_date, decryption_key)
        encrypted_address = encrypt_aes(address, decryption_key)
        encrypted_phone_number = encrypt_aes(phone_number, decryption_key)
        encrypted_position = encrypt_aes(position, decryption_key)

        # Update employee record
        employee.name = encrypted_name
        employee.birth_date = encrypted_birth_date
        employee.phone_number = encrypted_phone_number
        employee.address = encrypted_address
        employee.position = encrypted_position
        employee.save()

        # Return to employee list
        messages.success(request, "Chỉnh sửa thành công")
        return redirect('employee_list', department_id=employee.department_id)
    
    return render(request, 'records/employee_decrypt.html', {'employee': employee})


def department_list(request):
    departments = Department.objects.all()  # Lấy tất cả phòng ban
    return render(request, 'records/department_list.html', {'departments': departments})