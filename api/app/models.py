from pydantic import BaseModel
from typing import Optional, Dict, Any

class AuthRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    calling_station_id: Optional[str] = None

class RadiusResponse(BaseModel):
    control: Dict[str, Any] = {}
    reply: Dict[str, Any] = {}

class AcctRequest(BaseModel):
    acct_status_type: str
    acct_session_id: str
    username: Optional[str] = None
    nas_ip_address: str
    acct_session_time: Optional[int] = 0
    acct_input_octets: Optional[int] = 0
    acct_output_octets: Optional[int] = 0
    calling_station_id: Optional[str] = None
    called_station_id: Optional[str] = None
    acct_terminate_cause: Optional[str] = None
