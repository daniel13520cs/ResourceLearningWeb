# My Django Learning Resource Management App

Welcome to the Django Learning Resource Management App! This application allows users to manage learning resources, including creating, updating, deleting, and viewing resource details. Below is a guide on how to interact with the app and its features.

## Features

- **User Authentication**: Sign up, log in, and log out .
- **Learning Resource Management**: Create, update, delete, and view resources.
- **Image Handling**: Display resource images, including YouTube thumbnails.
- **Pagination**: Navigate through multiple pages of resources.
- **Responsive Design**: Mobile-friendly interface.
- **Opt-In for Public Events**: Users can opt-in to public events published by other users.

## Getting Started

### Prerequisites

- Python 3.x
- Django 3.x or later
- A web browser

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/your-repo.git
   cd your-repo
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run migrations**:
   ```bash
   python manage.py migrate
   ```

4. **Start the server**:
   ```bash
   python manage.py runserver
   ```

5. **Access the app**:
   Open your web browser and go to `http://127.0.0.1:8000/`.

![Getting Started](path/to/getting-started-image.png)

## Usage

### User Authentication

- **Sign Up**: Create a new account by clicking on the "Sign Up" button on the homepage.
  ![Sign Up](path/to/signup-image.png)

- **Log In**: Access your account by entering your credentials.
  ![Log In](path/to/login-image.png)

### Learning Resource Management

- **Create Resource**: Click on "Add New Resource" to create a new learning resource. Fill in the details and submit.
  ![Create Resource](path/to/create-resource-image.png)

- **View Resources**: Browse through the list of resources. Click on a resource to view more details.
  ![View Resources](path/to/view-resources-image.png)

- **Edit Resource**: If you are the owner, click "Edit" to modify resource details.
  ![Edit Resource](path/to/edit-resource-image.png)

- **Delete Resource**: Remove a resource by clicking "Delete".
  ![Delete Resource](path/to/delete-resource-image.png)

### Opt-In for Public Events

- **Opt-In to Public Events**: Users can opt-in to public events that other users have published. Look for the public events section and click "Opt In" to participate.
  ![Opt In Public Events](path/to/opt-in-public-events-image.png)

### Image Handling

- **Resource Images**: Upload an image for your resource or use a YouTube link to display a thumbnail.
  ![Resource Images](path/to/resource-images-image.png)

### Pagination

- **Navigate Pages**: Use the pagination controls at the bottom to navigate through resource pages.
  ![Pagination](path/to/pagination-image.png)

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please contact [daniel13520cs@gmail.com](mailto:your-email@example.com).