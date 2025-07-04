import re
from datetime import date, datetime, timedelta

from flask_login import AnonymousUserMixin as BaseAnonymousUserMixin
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from extensions import db


# AnonymousUserMixin에 has_permission 메서드 추가
class AnonymousUserMixin(BaseAnonymousUserMixin):
    """익명 사용자용 권한 체크 메서드"""

    def has_permission(self, module, action="view"):
        return False

    def get_permissions(self):
        return {}

    def get_permission_summary(self):
        return {"role": "anonymous", "grade": "none", "modules": {}}


# 지점 모델
class Branch(db.Model):
    __tablename__ = "branches"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    address = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    processing_time_standard = db.Column(
        db.Integer, default=15
    )  # 기준 주문 처리 시간(분)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self):
        return f"<Branch {self.name}>"


# User 모델
class User(db.Model, UserMixin):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(120), nullable=False)
    role = db.Column(
        db.String(20), default="employee", index=True
    )  # 'admin', 'manager', 'employee'
    grade = db.Column(
        db.String(20), default="staff", index=True
    )  # 'ceo', 'director', 'manager', 'staff'
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # 'approved', 'pending', 'rejected'
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), index=True)
    team_id = db.Column(db.Integer, db.ForeignKey("teams.id"), index=True)  # 팀 ID 추가
    deleted_at = db.Column(db.DateTime, nullable=True, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    attendances = db.relationship(
        "Attendance", backref="user", lazy=True, cascade="all, delete-orphan"
    )
    name = db.Column(db.String(50))
    phone = db.Column(db.String(20))
    last_login = db.Column(db.DateTime, index=True)

    # JSON 기반 세밀한 권한 관리
    permissions = db.Column(
        db.JSON,
        default=lambda: {
            # 대시보드 접근 권한
            "dashboard": {"view": True, "edit": False, "admin_only": False},
            # 직원 관리 권한
            "employee_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
                "assign_roles": False,
            },
            # 스케줄 관리 권한
            "schedule_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
            },
            # 발주 관리 권한
            "order_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
            },
            # 재고 관리 권한
            "inventory_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
            },
            # 알림 관리 권한
            "notification_management": {"view": False, "send": False, "delete": False},
            # 시스템 관리 권한
            "system_management": {
                "view": False,
                "backup": False,
                "restore": False,
                "settings": False,
                "monitoring": False,
            },
            # 보고서 권한
            "reports": {"view": False, "export": False, "admin_only": False},
        },
    )

    # 권한 위임 정보 (최고관리자가 매장관리자에게, 매장관리자가 직원에게)
    delegated_by = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    delegated_at = db.Column(db.DateTime, nullable=True)
    delegation_expires = db.Column(db.DateTime, nullable=True)

    # 관계 설정
    branch = db.relationship("Branch", backref="users")
    notifications = db.relationship("Notification", lazy="dynamic")
    delegated_users = db.relationship(
        "User",
        backref=db.backref("delegator", remote_side=[id]),
        foreign_keys=[delegated_by],
    )

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions = self._get_default_permissions()

    def _get_default_permissions(self):
        """역할별 기본 권한 설정"""
        base_permissions = {
            "dashboard": {"view": True, "edit": False, "admin_only": False},
            "employee_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
                "assign_roles": False,
            },
            "schedule_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
            },
            "order_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
                "approve": False,
            },
            "inventory_management": {
                "view": False,
                "create": False,
                "edit": False,
                "delete": False,
            },
            "notification_management": {"view": False, "send": False, "delete": False},
            "system_management": {
                "view": False,
                "backup": False,
                "restore": False,
                "settings": False,
                "monitoring": False,
            },
            "reports": {"view": False, "export": False, "admin_only": False},
        }

        if self.role == "admin":
            # 최고관리자: 모든 권한
            for module in base_permissions:
                for action in base_permissions[module]:
                    base_permissions[module][action] = True
        elif self.role == "manager":
            # 매장관리자: 제한된 관리 권한
            base_permissions["dashboard"]["view"] = True
            base_permissions["schedule_management"]["view"] = True
            base_permissions["schedule_management"]["create"] = True
            base_permissions["schedule_management"]["edit"] = True
            base_permissions["order_management"]["view"] = True
            base_permissions["order_management"]["create"] = True
            base_permissions["order_management"]["approve"] = True
            base_permissions["inventory_management"]["view"] = True
            base_permissions["inventory_management"]["create"] = True
            base_permissions["inventory_management"]["edit"] = True
            base_permissions["notification_management"]["view"] = True
            base_permissions["reports"]["view"] = True
        else:
            # 직원: 기본 업무 권한
            base_permissions["dashboard"]["view"] = True
            base_permissions["schedule_management"]["view"] = True
            base_permissions["order_management"]["view"] = True
            base_permissions["order_management"]["create"] = True
            base_permissions["inventory_management"]["view"] = True

        return base_permissions

    def has_permission(self, module, action):
        """특정 모듈의 특정 액션에 대한 권한 확인"""
        if not self.permissions:
            return False

        module_perms = self.permissions.get(module, {})

        # admin_only 체크
        if module_perms.get("admin_only", False) and self.role != "admin":
            return False

        # 특정 액션 권한 확인
        return module_perms.get(action, False)

    def can_access_module(self, module):
        """모듈 접근 권한 확인"""
        return self.has_permission(module, "view")

    def can_edit_module(self, module):
        """모듈 편집 권한 확인"""
        return self.has_permission(module, "edit")

    def can_create_in_module(self, module):
        """모듈 내 생성 권한 확인"""
        return self.has_permission(module, "create")

    def can_delete_in_module(self, module):
        """모듈 내 삭제 권한 확인"""
        return self.has_permission(module, "delete")

    def can_approve_in_module(self, module):
        """모듈 내 승인 권한 확인"""
        return self.has_permission(module, "approve")

    def delegate_permissions(self, target_user, permissions, expires_in_days=30):
        """권한 위임"""
        if not self.has_permission("employee_management", "assign_roles"):
            raise PermissionError("권한 위임 권한이 없습니다.")

        # 위임된 권한 설정
        target_user.permissions.update(permissions)
        target_user.delegated_by = self.id
        target_user.delegated_at = datetime.utcnow()
        target_user.delegation_expires = datetime.utcnow() + timedelta(
            days=expires_in_days
        )

        db.session.commit()

        # 위임 알림 발송
        from utils.notify import send_notification_enhanced

        send_notification_enhanced(
            user_id=target_user.id,
            title="권한이 위임되었습니다",
            content=f"{self.username}님이 {expires_in_days}일간 권한을 위임했습니다.",
        )

    def revoke_delegated_permissions(self, target_user):
        """위임된 권한 회수"""
        if target_user.delegated_by != self.id:
            raise PermissionError("해당 사용자의 권한을 회수할 수 없습니다.")

        # 기본 권한으로 복원
        target_user.permissions = target_user._get_default_permissions()
        target_user.delegated_by = None
        target_user.delegated_at = None
        target_user.delegation_expires = None

        db.session.commit()

        # 회수 알림 발송
        from utils.notify import send_notification_enhanced

        send_notification_enhanced(
            user_id=target_user.id,
            title="위임된 권한이 회수되었습니다",
            content=f"{self.username}님이 위임된 권한을 회수했습니다.",
        )

    def get_delegated_users(self):
        """위임받은 사용자 목록"""
        return User.query.filter_by(delegated_by=self.id).all()

    def is_delegation_expired(self):
        """위임 권한 만료 확인"""
        if not self.delegation_expires:
            return False
        return datetime.utcnow() > self.delegation_expires

    def get_effective_permissions(self):
        """실제 적용되는 권한 (만료 체크 포함)"""
        if self.is_delegation_expired():
            return self._get_default_permissions()
        return self.permissions

    def get_permission_summary(self):
        """권한 요약 정보"""
        perms = self.get_effective_permissions()
        summary = {"role": self.role, "grade": self.grade, "modules": {}}

        for module, actions in perms.items():
            summary["modules"][module] = {
                "can_access": actions.get("view", False),
                "can_edit": actions.get("edit", False),
                "can_create": actions.get("create", False),
                "can_delete": actions.get("delete", False),
                "can_approve": actions.get("approve", False),
            }

        return summary

    def set_password(self, pw):
        if len(pw) < 8:
            raise ValueError("비밀번호는 최소 8자 이상이어야 합니다.")
        if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
            raise ValueError("비밀번호는 영문자와 숫자를 포함해야 합니다.")
        self.password_hash = generate_password_hash(pw, method="pbkdf2:sha256")

    def check_password(self, pw):
        return check_password_hash(self.password_hash, pw)

    def is_admin(self):
        return self.role == "admin"

    def is_manager(self):
        return self.role == "manager"

    def is_employee(self):
        return self.role == "employee"

    def is_owner(self):
        """1인 사장님 여부 확인"""
        return self.role == "admin" and not self.is_group_admin()

    def is_group_admin(self):
        """그룹/프랜차이즈 최고관리자 여부 확인"""
        return self.role == "admin" and self.has_permission("group_admin")

    def is_solo_mode(self):
        """1인 사장님 모드에서 모든 메뉴 접근 가능 여부"""
        return self.is_owner() or self.has_permission("solo_mode")

    def is_franchise_mode(self):
        """그룹/프랜차이즈 모드에서 최고관리자 메뉴만 접근 가능 여부"""
        return self.is_group_admin() or self.has_permission("franchise_mode")

    def can_access_all_menus(self):
        """모든 메뉴에 접근 가능한지 확인 (1인 사장님 모드)"""
        return self.is_solo_mode()

    def can_access_admin_only_menus(self):
        """최고관리자 전용 메뉴에 접근 가능한지 확인 (그룹/프랜차이즈 모드)"""
        return self.is_franchise_mode()

    def get_dashboard_mode(self):
        """현재 사용자의 대시보드 모드 반환"""
        if self.is_solo_mode():
            return "solo"
        elif self.is_franchise_mode():
            return "franchise"
        else:
            return "employee"  # 일반 직원 모드

    def get_permissions(self):
        """현재 사용자의 모든 권한 반환"""
        return self.permissions or {}

    def set_permissions(self, permissions_dict):
        """권한 설정"""
        self.permissions = permissions_dict

    def add_permission(self, permission_name):
        """권한 추가"""
        if not self.permissions:
            self.permissions = {}
        self.permissions[permission_name] = True

    def remove_permission(self, permission_name):
        """권한 제거"""
        if self.permissions and permission_name in self.permissions:
            self.permissions[permission_name] = False

    @property
    def is_locked(self):
        if self.delegation_expires and self.delegation_expires > datetime.utcnow():
            return True
        return False

    def increment_login_attempts(self):
        self.login_attempts += 1
        if self.login_attempts >= 5:
            from datetime import timedelta

            self.delegation_expires = datetime.utcnow() + timedelta(minutes=30)
        db.session.commit()

    def reset_login_attempts(self):
        self.login_attempts = 0
        self.delegation_expires = None
        self.last_login = datetime.utcnow()
        db.session.commit()

    def __repr__(self):
        return f"<User {self.username}>"


# 출퇴근 모델
class Attendance(db.Model):
    __tablename__ = "attendances"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    clock_in = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )
    clock_out = db.Column(db.DateTime, index=True)
    location_in = db.Column(db.String(100))  # 출근 위치 (GPS 등)
    location_out = db.Column(db.String(100))  # 퇴근 위치
    notes = db.Column(db.Text)  # 메모
    reason = db.Column(db.String(200))  # 지각/조퇴/야근 사유 등
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_attendance_user_date", "user_id", "clock_in"),
        db.Index("idx_attendance_date_range", "clock_in", "clock_out"),
    )

    @property
    def work_minutes(self):
        if self.clock_in and self.clock_out:
            return int((self.clock_out - self.clock_in).total_seconds() // 60)
        return 0

    @property
    def work_hours(self):
        return round(self.work_minutes / 60, 2)

    @property
    def status(self):
        from datetime import time

        work_start = time(9, 0)
        work_end = time(18, 0)
        if not self.clock_in or not self.clock_out:
            return "결근" if not self.clock_in and not self.clock_out else "미완료"
        s = []
        if self.clock_in.time() > work_start:
            s.append("지각")
        if self.clock_out.time() < work_end:
            s.append("조퇴")
        if not s:
            return "정상"
        return "/".join(s)

    @property
    def is_late(self):
        from datetime import time

        work_start = time(9, 0)
        return self.clock_in and self.clock_in.time() > work_start

    @property
    def is_early_leave(self):
        from datetime import time

        work_end = time(18, 0)
        return self.clock_out and self.clock_out.time() < work_end

    @property
    def is_overtime(self):
        return self.work_hours > 8

    def __repr__(self):
        return f"<Attendance {self.user_id} {self.clock_in.date()}>"


# 액션로그
class ActionLog(db.Model):
    __tablename__ = "action_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    action = db.Column(db.String(50), nullable=False, index=True)
    message = db.Column(db.String(255))
    ip_address = db.Column(db.String(45))  # IPv6 지원
    user_agent = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_actionlog_user_action", "user_id", "action"),
        db.Index("idx_actionlog_action_date", "action", "created_at"),
    )

    def __repr__(self):
        return f"<ActionLog {self.user_id} {self.action}>"


# 피드백 모델
class Feedback(db.Model):
    __tablename__ = "feedback"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    satisfaction = db.Column(db.Integer)  # 1~5점
    health = db.Column(db.Integer)  # 1~5점
    comment = db.Column(db.String(500))  # 길이 증가
    category = db.Column(db.String(50))  # 피드백 카테고리
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def __repr__(self):
        return f"<Feedback {self.user_id} {self.satisfaction}>"


# 승인/거절 이력 로그
class ApproveLog(db.Model):
    __tablename__ = "approve_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    action = db.Column(
        db.String(32), nullable=False, index=True
    )  # 'approved' or 'rejected'
    timestamp = db.Column(db.DateTime, default=db.func.now(), index=True)
    admin_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )  # 처리자
    reason = db.Column(db.String(256))  # 선택: 승인/거절 사유 기록용 (옵션)
    ip_address = db.Column(db.String(45))

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_approvelog_user_action", "user_id", "action"),
        db.Index("idx_approvelog_admin_date", "admin_id", "timestamp"),
    )

    def __repr__(self):
        return f"<ApproveLog {self.user_id} {self.action} {self.timestamp}>"


# 근무 변경(교대) 신청 모델
class ShiftRequest(db.Model):
    __tablename__ = "shift_requests"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    request_date = db.Column(db.Date, nullable=False, index=True)  # 신청 날짜
    desired_date = db.Column(db.Date, nullable=False, index=True)  # 희망 날짜
    reason = db.Column(db.String(255), nullable=False)  # 사유
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # pending/approved/rejected
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now())

    # 관계 설정
    user = db.relationship("User", backref="shift_requests")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_shiftrequest_user_status", "user_id", "status"),
        db.Index("idx_shiftrequest_date_range", "request_date", "desired_date"),
    )

    def __repr__(self):
        return f"<ShiftRequest {self.user_id} {self.desired_date} {self.status}>"


# 알림 모델
class Notification(db.Model):
    __tablename__ = "notifications"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    content = db.Column(db.String(255), nullable=False)
    title = db.Column(db.String(100), nullable=True)  # 알림 제목 필드 추가
    category = db.Column(
        db.String(50), nullable=False, default="일반", index=True
    )  # 발주/청소/근무/교대/공지/일반
    related_url = db.Column(db.String(255), nullable=True)  # 알림 클릭 시 이동할 URL
    link = db.Column(db.String(255), nullable=True)  # 상세 페이지 링크 (별칭)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    is_read = db.Column(db.Boolean, default=False, index=True)
    is_admin_only = db.Column(
        db.Boolean, default=False, index=True
    )  # 관리자만 볼 수 있는 알림

    # 새로운 필드들 추가
    recipient_role = db.Column(db.String(20))  # ex. 'admin', 'manager', 'employee'
    recipient_team = db.Column(db.String(20))  # ex. '주방', '홀'
    priority = db.Column(
        db.String(10), default="일반", index=True
    )  # '긴급', '중요', '일반'
    ai_priority = db.Column(db.String(10), index=True)  # AI가 추천한 우선순위

    # 관계 설정
    user = db.relationship("User")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_notification_user_read", "user_id", "is_read"),
        db.Index("idx_notification_category_date", "category", "created_at"),
        db.Index("idx_notification_priority_date", "priority", "created_at"),
        db.Index("idx_notification_team_role", "recipient_team", "recipient_role"),
    )

    def __repr__(self):
        return f"<Notification {self.id} {self.content[:20]}>"


# 공지사항 모델
class Notice(db.Model):
    __tablename__ = "notices"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    file_path = db.Column(db.String(255))  # 첨부파일 경로
    file_type = db.Column(db.String(20))  # 파일 확장자
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    author_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    category = db.Column(db.String(30), index=True)  # 공지사항, 자료실 등
    is_hidden = db.Column(db.Boolean, default=False, index=True)  # 숨김 처리 여부

    # 관계 설정
    author = db.relationship("User", backref="notices")
    reads = db.relationship(
        "NoticeRead", backref="notice", cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "NoticeComment", backref="notice", cascade="all, delete-orphan"
    )

    __table_args__ = (
        db.Index("idx_notice_author_category", "author_id", "category"),
        db.Index("idx_notice_created", "created_at"),
    )

    def __repr__(self):
        return f"<Notice {self.title}>"


class NoticeRead(db.Model):
    __tablename__ = "notice_reads"
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(
        db.Integer, db.ForeignKey("notices.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    read_at = db.Column(db.DateTime, default=db.func.now(), index=True)

    # 복합 인덱스 추가
    __table_args__ = (
        db.UniqueConstraint("notice_id", "user_id", name="uq_notice_user"),
        db.Index("idx_noticeread_user_notice", "user_id", "notice_id"),
    )

    def __repr__(self):
        return f"<NoticeRead {self.user_id} read {self.notice_id}>"


class NoticeComment(db.Model):
    __tablename__ = "notice_comments"
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(
        db.Integer, db.ForeignKey("notices.id"), nullable=False, index=True
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    is_hidden = db.Column(db.Boolean, default=False, index=True)  # 숨김 처리 여부

    # 관계 설정
    user = db.relationship("User", backref="notice_comments")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_noticecomment_notice_user", "notice_id", "user_id"),
        db.Index("idx_noticecomment_created", "created_at"),
    )

    def __repr__(self):
        return f"<NoticeComment {self.id} on notice {self.notice_id}>"


class NoticeHistory(db.Model):
    __tablename__ = "notice_histories"
    id = db.Column(db.Integer, primary_key=True)
    notice_id = db.Column(
        db.Integer, db.ForeignKey("notices.id"), nullable=False, index=True
    )
    editor_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    before_title = db.Column(db.String(100))
    before_content = db.Column(db.Text)
    before_file_path = db.Column(db.String(255))
    before_file_type = db.Column(db.String(20))
    edited_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    action = db.Column(db.String(10), index=True)  # 'edit'/'delete'/'hide'/'unhide'
    ip_address = db.Column(db.String(45))

    # 관계 설정
    editor = db.relationship("User", backref="notice_histories")
    notice = db.relationship("Notice", backref="histories")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_noticehistory_notice", "notice_id"),
        db.Index("idx_noticehistory_editor", "editor_id"),
    )

    def __repr__(self):
        return f"<NoticeHistory {self.id} for notice {self.notice_id}>"


class CommentHistory(db.Model):
    __tablename__ = "comment_histories"
    id = db.Column(db.Integer, primary_key=True)
    comment_id = db.Column(
        db.Integer, db.ForeignKey("notice_comments.id"), nullable=False, index=True
    )
    editor_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    before_content = db.Column(db.Text)
    edited_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    action = db.Column(db.String(10), index=True)  # 'edit'/'delete'/'hide'/'unhide'
    ip_address = db.Column(db.String(45))

    # 관계 설정
    editor = db.relationship("User", backref="comment_histories")
    comment = db.relationship("NoticeComment", backref="histories")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_commenthistory_comment", "comment_id"),
        db.Index("idx_commenthistory_editor", "editor_id"),
    )

    def __repr__(self):
        return f"<CommentHistory {self.id} for comment {self.comment_id}>"


class Report(db.Model):
    __tablename__ = "reports"
    id = db.Column(db.Integer, primary_key=True)
    target_type = db.Column(
        db.String(10), nullable=False, index=True
    )  # 'notice'/'comment'
    target_id = db.Column(db.Integer, nullable=False, index=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    reason = db.Column(db.String(100), nullable=False)
    category = db.Column(
        db.String(20), index=True
    )  # '욕설/비방', '음란', '홍보', '기타'
    detail = db.Column(db.Text)  # 상세 사유
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # 'pending'/'reviewed'/'resolved'
    admin_comment = db.Column(db.Text)  # 관리자 처리 코멘트
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    reviewed_at = db.Column(db.DateTime, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)

    # 관계 설정
    reporter = db.relationship("User", foreign_keys=[user_id], backref="reports")
    reviewer = db.relationship(
        "User", foreign_keys=[reviewed_by], backref="reviewed_reports"
    )

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_report_target", "target_type", "target_id"),
        db.Index("idx_report_status_category", "status", "category"),
    )

    def __repr__(self):
        return f"<Report {self.id} for {self.target_type} {self.target_id}>"


class SystemLog(db.Model):
    """시스템 로그 모델"""

    __tablename__ = "system_logs"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    detail = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(500), nullable=True)
    created_at = db.Column(db.DateTime, default=db.func.now())

    # 관계 설정
    user = db.relationship("User", backref="system_logs")

    def __repr__(self):
        return f"<SystemLog {self.action} by User {self.user_id}>"


class Suggestion(db.Model):
    __tablename__ = "suggestions"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    content = db.Column(db.Text, nullable=False)
    answer = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now(), index=True)
    answered_at = db.Column(db.DateTime, index=True)
    is_anonymous = db.Column(db.Boolean, default=True, index=True)

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_suggestion_created", "created_at"),
        db.Index("idx_suggestion_answered", "answered_at"),
    )

    def __repr__(self):
        return f"<Suggestion {self.id}>"


class Schedule(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=True
    )  # 직원 근무 시
    branch_id = db.Column(
        db.Integer, db.ForeignKey("branches.id"), nullable=True
    )  # 매장 정보
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    type = db.Column(db.String(16), default="work")  # 'work', 'clean'
    category = db.Column(db.String(50), nullable=False, default="근무")
    status = db.Column(
        db.String(20), nullable=False, default="대기"
    )  # 대기, 승인, 거절
    memo = db.Column(db.String(200), nullable=True)
    team = db.Column(db.String(30))  # 청소 담당 팀 (ex: "주방", "홀")
    plan = db.Column(db.String(200))  # 청소 계획 내용
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 담당자(청소 시)

    user = db.relationship(
        "User", foreign_keys=[user_id], backref=db.backref("schedules", lazy=True)
    )
    branch = db.relationship("Branch", backref="schedules")
    manager = db.relationship(
        "User", foreign_keys=[manager_id], backref="managed_schedules"
    )

    def __repr__(self):
        return f"<Schedule {self.date} {self.type} {self.user_id}>"


class CleaningPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date)
    plan = db.Column(db.String(200), nullable=False)
    team = db.Column(db.String(30))  # ex: "주방", "홀" 등
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 담당자(옵션)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 담당 직원

    user = db.relationship(
        "User", foreign_keys=[user_id], backref="cleaning_assignments"
    )
    manager = db.relationship(
        "User", foreign_keys=[manager_id], backref="managed_cleaning_plans"
    )

    def __repr__(self):
        return f"<CleaningPlan {self.date} {self.plan}>"


class Order(db.Model):
    """발주 모델"""

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    item = db.Column(db.String(200), nullable=False)  # 물품명
    quantity = db.Column(db.Integer, nullable=False, default=1)  # 수량
    order_date = db.Column(db.Date, nullable=False, default=date.today)  # 발주 날짜
    ordered_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False
    )  # 발주자
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # pending/approved/rejected/delivered
    detail = db.Column(db.String(500))  # 상세 설명
    memo = db.Column(db.String(500))  # 메모
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    completed_at = db.Column(db.DateTime)
    processing_minutes = db.Column(db.Integer)
    employee_id = db.Column(db.Integer, db.ForeignKey("users.id"))  # 직원
    store_id = db.Column(db.Integer, db.ForeignKey("branches.id"))  # 매장
    # 관계 설정
    user = db.relationship("User", foreign_keys=[ordered_by])

    def __repr__(self):
        return f"<Order {self.item} {self.quantity}>"


class AttendanceEvaluation(db.Model):
    """근태 평가 모델"""

    __tablename__ = "attendance_evaluations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    date_from = db.Column(db.Date, nullable=False, index=True)
    date_to = db.Column(db.Date, nullable=False, index=True)
    total_days = db.Column(db.Integer, default=0)
    late_count = db.Column(db.Integer, default=0)
    early_leave_count = db.Column(db.Integer, default=0)
    overtime_count = db.Column(db.Integer, default=0)
    normal_count = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)  # 0-100점
    grade = db.Column(db.String(5), default="D")  # A+, A, B+, B, C+, C, D
    comment = db.Column(db.Text)  # 관리자 평가 코멘트
    evaluator_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 관계 설정
    user = db.relationship(
        "User", foreign_keys=[user_id], backref="attendance_evaluations"
    )
    evaluator = db.relationship(
        "User", foreign_keys=[evaluator_id], backref="evaluated_attendance"
    )

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index(
            "idx_attendance_evaluation_user_period", "user_id", "date_from", "date_to"
        ),
        db.Index("idx_attendance_evaluation_score", "score"),
        db.Index("idx_attendance_evaluation_grade", "grade"),
    )

    def __repr__(self):
        return f"<AttendanceEvaluation {self.user_id} {self.date_from}~{self.date_to} {self.grade}>"


class AttendanceReport(db.Model):
    """근태 평가 리포트 모델"""

    __tablename__ = "attendance_reports"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    period_from = db.Column(db.Date, nullable=False)
    period_to = db.Column(db.Date, nullable=False)
    total = db.Column(db.Integer, default=0)
    late = db.Column(db.Integer, default=0)
    early = db.Column(db.Integer, default=0)
    ot = db.Column(db.Integer, default=0)
    ontime = db.Column(db.Integer, default=0)
    score = db.Column(db.Integer, default=0)
    grade = db.Column(db.String(10), default="")
    comment = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    warning = db.Column(db.Boolean, default=False)  # 경고 여부 추가

    # 관계
    user = db.relationship("User", foreign_keys=[user_id], backref="attendance_reports")
    creator = db.relationship(
        "User", foreign_keys=[created_by], backref="created_reports"
    )

    def __repr__(self):
        return f"<AttendanceReport {self.user_id} {self.period_from}~{self.period_to}>"


class ReasonTemplate(db.Model):
    """근태 사유 템플릿 모델"""

    __tablename__ = "reason_templates"

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(100), unique=True, nullable=False, comment="사유 텍스트")
    team = db.Column(db.String(30), comment="팀별 템플릿(옵션)")
    status = db.Column(
        db.String(20), default="pending", comment="승인 상태: pending/approved/rejected"
    )
    is_active = db.Column(db.Boolean, default=True, comment="활성화 여부")
    created_by = db.Column(db.Integer, db.ForeignKey("users.id"), comment="생성자")
    approved_by = db.Column(db.Integer, db.ForeignKey("users.id"), comment="승인자")
    approved_at = db.Column(db.DateTime, comment="승인일시")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정일시",
    )
    approval_comment = db.Column(db.String(200))  # 승인/거절 코멘트

    # 관계
    creator = db.relationship(
        "User", foreign_keys=[created_by], backref="created_templates"
    )
    approver = db.relationship(
        "User", foreign_keys=[approved_by], backref="approved_templates"
    )

    def __repr__(self):
        return f"<ReasonTemplate {self.text}>"


class ReasonEditLog(db.Model):
    """근태 사유 변경 이력 모델"""

    __tablename__ = "reason_edit_logs"

    id = db.Column(db.Integer, primary_key=True)
    attendance_id = db.Column(
        db.Integer,
        db.ForeignKey("attendances.id"),
        nullable=False,
        comment="근태 기록 ID",
    )
    old_reason = db.Column(db.String(200), comment="이전 사유")
    new_reason = db.Column(db.String(200), comment="새 사유")
    edited_by = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, comment="수정자"
    )
    edited_at = db.Column(db.DateTime, default=datetime.utcnow, comment="수정일시")
    ip_address = db.Column(db.String(45), comment="IP 주소")
    user_agent = db.Column(db.String(500), comment="사용자 에이전트")

    # 관계
    attendance = db.relationship("Attendance", backref="reason_edit_logs")
    editor = db.relationship("User", backref="reason_edits")

    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_reason_edit_attendance", "attendance_id"),
        db.Index("idx_reason_edit_editor", "edited_by"),
        db.Index("idx_reason_edit_date", "edited_at"),
    )

    def __repr__(self):
        return f"<ReasonEditLog {self.attendance_id} {self.edited_at}>"


class Excuse(db.Model):
    """소명(이의제기) 모델"""

    __tablename__ = "excuses"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    attendance_report_id = db.Column(
        db.Integer, db.ForeignKey("attendance_reports.id"), nullable=True, index=True
    )
    attendance_evaluation_id = db.Column(
        db.Integer,
        db.ForeignKey("attendance_evaluations.id"),
        nullable=True,
        index=True,
    )
    title = db.Column(db.String(200), nullable=False, comment="소명 제목")
    content = db.Column(db.Text, nullable=False, comment="소명 내용")
    status = db.Column(
        db.String(20),
        default="pending",
        index=True,
        comment="상태: pending/reviewed/accepted/rejected",
    )
    priority = db.Column(
        db.String(10), default="일반", index=True, comment="우선순위: 긴급/중요/일반"
    )
    category = db.Column(db.String(50), default="근태평가", comment="소명 카테고리")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    reviewed_at = db.Column(db.DateTime, index=True)
    reviewed_by = db.Column(db.Integer, db.ForeignKey("users.id"), index=True)
    admin_comment = db.Column(db.Text, comment="관리자 답변")

    # 관계
    user = db.relationship("User", foreign_keys=[user_id], backref="excuses")
    reviewer = db.relationship(
        "User", foreign_keys=[reviewed_by], backref="reviewed_excuses"
    )
    attendance_report = db.relationship("AttendanceReport", backref="excuses")
    attendance_evaluation = db.relationship("AttendanceEvaluation", backref="excuses")

    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_excuse_user_status", "user_id", "status"),
        db.Index("idx_excuse_status_date", "status", "created_at"),
        db.Index("idx_excuse_reviewer_date", "reviewed_by", "reviewed_at"),
    )

    def __repr__(self):
        return f"<Excuse {self.user_id} {self.title}>"


class ExcuseResponse(db.Model):
    """소명 답변 모델"""

    __tablename__ = "excuse_responses"

    id = db.Column(db.Integer, primary_key=True)
    excuse_id = db.Column(
        db.Integer, db.ForeignKey("excuses.id"), nullable=False, index=True
    )
    responder_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    content = db.Column(db.Text, nullable=False, comment="답변 내용")
    response_type = db.Column(
        db.String(20),
        default="comment",
        index=True,
        comment="답변 유형: comment/decision/request",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 관계
    excuse = db.relationship("Excuse", backref="responses")
    responder = db.relationship("User", backref="excuse_responses")

    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_excuseresponse_excuse_date", "excuse_id", "created_at"),
        db.Index("idx_excuseresponse_responder_date", "responder_id", "created_at"),
    )

    def __repr__(self):
        return f"<ExcuseResponse {self.excuse_id} {self.responder_id}>"


class Team(db.Model):
    """팀 모델"""

    __tablename__ = "teams"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False, comment="팀명")
    description = db.Column(db.String(200), comment="팀 설명")
    manager_id = db.Column(db.Integer, db.ForeignKey("users.id"), comment="팀장 ID")
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"), comment="소속 지점")
    is_active = db.Column(db.Boolean, default=True, comment="활성화 여부")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정일시",
    )
    permissions = db.Column(db.JSON, default=dict)

    # 관계
    manager = db.relationship(
        "User", foreign_keys=[manager_id], backref="managed_teams"
    )
    branch = db.relationship("Branch", backref="teams")
    members = db.relationship("User", backref="team", foreign_keys="User.team_id")

    def __repr__(self):
        return f"<Team {self.name}>"


class PermissionChangeLog(db.Model):
    """권한 변경 로그 모델"""

    __tablename__ = "permission_change_logs"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="권한 변경 대상",
    )
    changed_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="권한 변경자",
    )
    change_type = db.Column(
        db.String(20),
        nullable=False,
        index=True,
        comment="변경 유형: role/permission/delegation",
    )
    before_value = db.Column(db.String(500), comment="변경 전 값")
    after_value = db.Column(db.String(500), comment="변경 후 값")
    reason = db.Column(db.String(200), comment="변경 사유")
    ip_address = db.Column(db.String(45), comment="IP 주소")
    user_agent = db.Column(db.String(500), comment="사용자 에이전트")
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, index=True, comment="변경일시"
    )

    # 관계
    user = db.relationship("User", foreign_keys=[user_id], backref="permission_changes")
    changer = db.relationship(
        "User", foreign_keys=[changed_by], backref="permission_changes_made"
    )

    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_permissionlog_user_date", "user_id", "created_at"),
        db.Index("idx_permissionlog_changer_date", "changed_by", "created_at"),
        db.Index("idx_permissionlog_type_date", "change_type", "created_at"),
    )

    def __repr__(self):
        return f"<PermissionChangeLog {self.user_id} {self.change_type}>"


class UserPermission(db.Model):
    """사용자 권한 모델"""

    __tablename__ = "user_permissions"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="사용자 ID",
    )
    permission_name = db.Column(
        db.String(50), nullable=False, index=True, comment="권한명"
    )
    is_active = db.Column(db.Boolean, default=True, comment="활성화 여부")
    granted_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="권한 부여자",
    )
    granted_at = db.Column(
        db.DateTime, default=datetime.utcnow, comment="권한 부여일시"
    )
    expires_at = db.Column(db.DateTime, nullable=True, comment="권한 만료일시")
    reason = db.Column(db.String(200), comment="권한 부여 사유")

    # 관계
    user = db.relationship("User", foreign_keys=[user_id], backref="user_permissions")
    granter = db.relationship(
        "User", foreign_keys=[granted_by], backref="granted_permissions"
    )

    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_userpermission_user_name", "user_id", "permission_name"),
        db.Index("idx_userpermission_granter_date", "granted_by", "granted_at"),
        db.Index("idx_userpermission_active_expires", "is_active", "expires_at"),
    )

    def __repr__(self):
        return f"<UserPermission {self.user_id} {self.permission_name}>"


class PermissionTemplate(db.Model):
    """권한 템플릿 모델"""

    __tablename__ = "permission_templates"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, comment="템플릿명")
    description = db.Column(db.String(200), comment="템플릿 설명")
    permissions = db.Column(db.String(500), comment="권한 목록 (JSON)")
    role_type = db.Column(
        db.String(20), index=True, comment="역할 유형: manager/teamlead/employee"
    )
    is_active = db.Column(db.Boolean, default=True, comment="활성화 여부")
    created_by = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False,
        index=True,
        comment="생성자",
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, comment="생성일시")
    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        comment="수정일시",
    )

    # 관계
    creator = db.relationship("User", backref="created_permission_templates")

    def __repr__(self):
        return f"<PermissionTemplate {self.name}>"


class FeedbackIssue(db.Model):
    __tablename__ = "feedback_issues"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"))
    status = db.Column(
        db.String(32), default="pending"
    )  # 'pending', 'in_progress', 'resolved'

    user = db.relationship("User", backref="feedback_issues")
    branch = db.relationship("Branch", backref="feedback_issues")

    def __repr__(self):
        return f"<FeedbackIssue {self.title}>"


class RestaurantOrder(db.Model):
    """레스토랑 주문 처리 시간 측정 모델"""

    __tablename__ = "restaurant_orders"
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(
        db.String(50), unique=True, nullable=False, index=True
    )  # 주문번호
    customer_name = db.Column(db.String(100))  # 고객명
    order_items = db.Column(db.Text, nullable=False)  # 주문 메뉴 (JSON 형태)
    total_amount = db.Column(db.Integer, nullable=False)  # 총 금액
    status = db.Column(
        db.String(20), default="pending", index=True
    )  # pending/processing/completed/cancelled

    # 처리 시간 관련 필드
    created_at = db.Column(
        db.DateTime, default=datetime.utcnow, nullable=False, index=True
    )  # 주문 생성 시간
    completed_at = db.Column(db.DateTime, index=True)  # 처리 완료 시간
    processing_minutes = db.Column(db.Integer, index=True)  # 처리 소요 시간(분)

    # 매장/직원 정보
    store_id = db.Column(
        db.Integer, db.ForeignKey("branches.id"), nullable=False, index=True
    )
    employee_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )  # 처리 직원

    # 추가 정보
    notes = db.Column(db.Text)  # 메모
    payment_method = db.Column(db.String(20), default="cash")  # 결제 방법
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    # 관계 설정
    store = db.relationship("Branch", backref="restaurant_orders")
    employee = db.relationship("User", backref="processed_orders")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_restaurant_order_store_status", "store_id", "status"),
        db.Index("idx_restaurant_order_employee_date", "employee_id", "created_at"),
        db.Index("idx_restaurant_order_processing_time", "processing_minutes"),
        db.Index(
            "idx_restaurant_order_created_completed", "created_at", "completed_at"
        ),
    )

    def __repr__(self):
        return f"<RestaurantOrder {self.order_number} {self.status}>"

    @property
    def is_over_standard(self):
        """기준 시간 초과 여부 확인"""
        if not self.processing_minutes or not self.store:
            return False
        return self.processing_minutes > self.store.processing_time_standard

    @property
    def standard_time(self):
        """매장별 기준 시간 반환"""
        return self.store.processing_time_standard if self.store else 15


class OrderFeedback(db.Model):
    """주문 처리 경고/칭찬 피드백 모델"""

    __tablename__ = "order_feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(
        db.Integer, db.ForeignKey("orders.id"), nullable=False, index=True
    )
    employee_id = db.Column(
        db.Integer, db.ForeignKey("users.id"), nullable=False, index=True
    )
    type = db.Column(db.String(16), nullable=False, index=True)  # 'warn', 'praise'
    message = db.Column(db.String(256), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    # 관계 설정
    order = db.relationship("Order", backref="feedbacks")
    employee = db.relationship("User", backref="order_feedbacks")

    # 복합 인덱스 추가
    __table_args__ = (
        db.Index("idx_orderfeedback_employee_type", "employee_id", "type"),
        db.Index("idx_orderfeedback_created", "created_at"),
    )

    def __repr__(self):
        return f"<OrderFeedback {self.id} {self.type} for Order {self.order_id}>"


class OrderRequest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(128))
    quantity = db.Column(db.Integer)
    status = db.Column(
        db.String(32), default="pending"
    )  # 'pending', 'approved', 'completed'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    requested_by = db.Column(db.Integer, db.ForeignKey("users.id"))
    branch_id = db.Column(db.Integer, db.ForeignKey("branches.id"))
    # 관계
    user = db.relationship("User", foreign_keys=[requested_by])
    branch = db.relationship("Branch", foreign_keys=[branch_id])
    # 기타 필요 항목 자유롭게 추가


class PayTransfer(db.Model):
    """급여 이체 모델"""
    __tablename__ = "pay_transfers"
    
    id = db.Column(db.Integer, primary_key=True)
    from_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    to_user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    amount = db.Column(db.Integer, nullable=False)  # 이체 금액
    description = db.Column(db.String(200))  # 이체 설명
    status = db.Column(db.String(20), default="pending", index=True)  # pending/completed/failed
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    completed_at = db.Column(db.DateTime, index=True)
    
    # 관계 설정
    from_user = db.relationship("User", foreign_keys=[from_user_id], backref="sent_transfers")
    to_user = db.relationship("User", foreign_keys=[to_user_id], backref="received_transfers")
    
    # 복합 인덱스
    __table_args__ = (
        db.Index("idx_transfer_users", "from_user_id", "to_user_id"),
        db.Index("idx_transfer_status", "status", "created_at"),
    )
    
    def __repr__(self):
        return f"<PayTransfer {self.from_user_id} -> {self.to_user_id}: {self.amount}원>"


class Payroll(db.Model):
    """급여 모델"""
    __tablename__ = "payrolls"
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, index=True)
    year = db.Column(db.Integer, nullable=False, index=True)
    month = db.Column(db.Integer, nullable=False, index=True)
    base_salary = db.Column(db.Integer, default=0)  # 기본급
    allowance = db.Column(db.Integer, default=0)  # 수당
    deduction = db.Column(db.Integer, default=0)  # 공제
    net_salary = db.Column(db.Integer, default=0)  # 실수령액
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    user = db.relationship("User", backref="payrolls")
    
    # 복합 인덱스
    __table_args__ = (
        db.Index('idx_payroll_user_year_month', 'user_id', 'year', 'month'),
    )
    
    def __repr__(self):
        return f"<Payroll {self.user_id} {self.year}-{self.month}>"


class Staff(db.Model):
    """직원 모델"""
    __tablename__ = "staff"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    position = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120))
    status = db.Column(db.String(20), default="active", index=True)  # active, on_leave, inactive
    avatar = db.Column(db.String(255))  # 프로필 이미지 경로
    join_date = db.Column(db.Date, nullable=False)
    salary = db.Column(db.String(50))  # 급여 정보
    department = db.Column(db.String(100))
    restaurant_id = db.Column(db.Integer, db.ForeignKey("branches.id"), nullable=False, index=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True, index=True)  # 시스템 사용자와 연결
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 관계 설정
    restaurant = db.relationship("Branch", backref="staff")
    user = db.relationship("User", backref="staff_profile")
    contracts = db.relationship("Contract", backref="staff", cascade="all, delete-orphan")
    health_certificates = db.relationship("HealthCertificate", backref="staff", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<Staff {self.name}>"


class Contract(db.Model):
    """계약서 모델"""
    __tablename__ = "contracts"
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False, index=True)
    contract_number = db.Column(db.String(50), unique=True, nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False, index=True)
    renewal_date = db.Column(db.Date, nullable=False)
    contract_type = db.Column(db.String(50), default="정규직")  # 정규직, 계약직, 파트타임 등
    salary_amount = db.Column(db.Integer)  # 계약 급여
    file_path = db.Column(db.String(255))  # 계약서 파일 경로
    file_name = db.Column(db.String(255))  # 원본 파일명
    file_size = db.Column(db.Integer)  # 파일 크기 (bytes)
    notification_sent = db.Column(db.Boolean, default=False, index=True)  # 만료 임박 알림 발송 여부
    expired_notification_sent = db.Column(db.Boolean, default=False, index=True)  # 만료 알림 발송 여부
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 복합 인덱스
    __table_args__ = (
        db.Index('idx_contract_expiry_notification', 'expiry_date', 'notification_sent'),
        db.Index('idx_contract_expired_notification', 'expiry_date', 'expired_notification_sent'),
    )
    
    @property
    def is_expiring_soon(self):
        """30일 이내에 만료되는지 확인"""
        today = datetime.now().date()
        return self.expiry_date <= today + timedelta(days=30) and self.expiry_date > today
    
    @property
    def is_expired(self):
        """만료되었는지 확인"""
        return self.expiry_date <= datetime.now().date()
    
    @property
    def days_until_expiry(self):
        """만료까지 남은 일수"""
        today = datetime.now().date()
        return (self.expiry_date - today).days
    
    def __repr__(self):
        return f"<Contract {self.contract_number} - {self.staff.name}>"


class HealthCertificate(db.Model):
    """보건증 모델"""
    __tablename__ = "health_certificates"
    
    id = db.Column(db.Integer, primary_key=True)
    staff_id = db.Column(db.Integer, db.ForeignKey("staff.id"), nullable=False, index=True)
    certificate_number = db.Column(db.String(50), unique=True, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    expiry_date = db.Column(db.Date, nullable=False, index=True)
    renewal_date = db.Column(db.Date, nullable=False)
    issuing_authority = db.Column(db.String(100))  # 발급 기관
    certificate_type = db.Column(db.String(50), default="식품위생교육")  # 보건증 유형
    file_path = db.Column(db.String(255))  # 보건증 파일 경로
    file_name = db.Column(db.String(255))  # 원본 파일명
    file_size = db.Column(db.Integer)  # 파일 크기 (bytes)
    notification_sent = db.Column(db.Boolean, default=False, index=True)  # 만료 임박 알림 발송 여부
    expired_notification_sent = db.Column(db.Boolean, default=False, index=True)  # 만료 알림 발송 여부
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 복합 인덱스
    __table_args__ = (
        db.Index('idx_health_cert_expiry_notification', 'expiry_date', 'notification_sent'),
        db.Index('idx_health_cert_expired_notification', 'expiry_date', 'expired_notification_sent'),
    )
    
    @property
    def is_expiring_soon(self):
        """30일 이내에 만료되는지 확인"""
        today = datetime.now().date()
        return self.expiry_date <= today + timedelta(days=30) and self.expiry_date > today
    
    @property
    def is_expired(self):
        """만료되었는지 확인"""
        return self.expiry_date <= datetime.now().date()
    
    @property
    def days_until_expiry(self):
        """만료까지 남은 일수"""
        today = datetime.now().date()
        return (self.expiry_date - today).days
    
    def __repr__(self):
        return f"<HealthCertificate {self.certificate_number} - {self.staff.name}>"
