from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, IoTDevice, IoTData
from datetime import datetime, timedelta
import random

iot_bp = Blueprint('iot', __name__)

# IoT 센서 데이터 수집 API
@iot_bp.route('/api/iot/data', methods=['POST'])
@login_required
def collect_iot_data():
    data = request.get_json()
    device_id = data.get('device_id')
    data_type = data.get('data_type')
    value = data.get('value')
    extra = data.get('extra', {})

    if not device_id or not data_type:
        return jsonify({'error': 'device_id와 data_type이 필요합니다.'}), 400

    iot_data = IoTData(
        device_id=device_id,
        data_type=data_type,
        value=value,
        extra=extra,
        timestamp=datetime.utcnow()
    )
    db.session.add(iot_data)
    db.session.commit()
    return jsonify({'success': True, 'id': iot_data.id})

# IoT 실시간 데이터 조회 API
@iot_bp.route('/api/iot/monitor', methods=['GET'])
@login_required
def get_iot_monitor():
    # 최근 10분 이내 데이터만 조회
    since = datetime.utcnow() - timedelta(minutes=10)
    data = IoTData.query.filter(IoTData.timestamp >= since).all()
    result = [
        {
            'id': d.id,
            'device_id': d.device_id,
            'data_type': d.data_type,
            'value': d.value,
            'extra': d.extra,
            'timestamp': d.timestamp.isoformat()
        }
        for d in data
    ]
    return jsonify({'success': True, 'data': result})

# IoT 장치 목록 조회
@iot_bp.route('/api/iot/devices', methods=['GET'])
@login_required
def get_iot_devices():
    devices = IoTDevice.query.all()
    result = [
        {
            'id': d.id,
            'name': d.name,
            'device_type': d.device_type,
            'location': d.location,
            'description': d.description,
            'created_at': d.created_at.isoformat()
        }
        for d in devices
    ]
    return jsonify({'success': True, 'devices': result})

# IoT 더미 데이터 시뮬레이터 (테스트용)
@iot_bp.route('/api/iot/simulate', methods=['POST'])
@login_required
def simulate_iot_data():
    # 임의의 더미 데이터 생성
    device_types = ['temperature', 'humidity', 'inventory', 'machine']
    for device_type in device_types:
        device = IoTDevice.query.filter_by(device_type=device_type).first()
        if not device:
            device = IoTDevice(
                name=f'{device_type.capitalize()} Sensor',
                device_type=device_type,
                location='매장1',
                description=f'{device_type} 센서'
            )
            db.session.add(device)
            db.session.commit()
        value = None
        if device_type == 'temperature':
            value = round(random.uniform(18, 28), 1)
        elif device_type == 'humidity':
            value = round(random.uniform(30, 70), 1)
        elif device_type == 'inventory':
            value = random.randint(10, 100)
        elif device_type == 'machine':
            value = random.choice([0, 1])  # 0: off, 1: on
        iot_data = IoTData(
            device_id=device.id,
            data_type=device_type,
            value=value,
            extra={'status': 'ok'},
            timestamp=datetime.utcnow()
        )
        db.session.add(iot_data)
    db.session.commit()
    return jsonify({'success': True, 'message': '더미 IoT 데이터가 생성되었습니다.'}) 