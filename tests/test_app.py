import pytest

def test_root_redirect(client):
    """Test that root endpoint serves the index page"""
    # Arrange - no special setup needed
    
    # Act
    response = client.get("/")
    
    # Assert
    assert response.status_code == 200
    assert "Mergington High School" in response.text

def test_get_activities(client):
    """Test retrieving all activities"""
    # Arrange - activities are reset by fixture
    
    # Act
    response = client.get("/activities")
    
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    # Verify structure
    chess_club = data["Chess Club"]
    assert "description" in chess_club
    assert "schedule" in chess_club
    assert "max_participants" in chess_club
    assert "participants" in chess_club
    assert isinstance(chess_club["participants"], list)

def test_signup_success(client):
    """Test successful signup for an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "newstudent@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify participant was added
    response2 = client.get("/activities")
    data = response2.json()
    assert email in data[activity_name]["participants"]

def test_signup_duplicate_participant(client):
    """Test signup fails when student is already signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already in Chess Club
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"]

def test_signup_nonexistent_activity(client):
    """Test signup fails for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.post(f"/activities/{activity_name}/signup?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]

def test_unregister_success(client):
    """Test successful unregister from an activity"""
    # Arrange
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already signed up
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 200
    result = response.json()
    assert "message" in result
    assert "Unregistered" in result["message"]
    
    # Verify participant was removed
    response2 = client.get("/activities")
    data = response2.json()
    assert email not in data[activity_name]["participants"]

def test_unregister_not_signed_up(client):
    """Test unregister fails when student is not signed up"""
    # Arrange
    activity_name = "Chess Club"
    email = "notsigned@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 400
    result = response.json()
    assert "detail" in result
    assert "not signed up" in result["detail"]

def test_unregister_nonexistent_activity(client):
    """Test unregister fails for non-existent activity"""
    # Arrange
    activity_name = "NonExistent Club"
    email = "student@mergington.edu"
    
    # Act
    response = client.delete(f"/activities/{activity_name}/unregister?email={email}")
    
    # Assert
    assert response.status_code == 404
    result = response.json()
    assert "detail" in result
    assert "Activity not found" in result["detail"]