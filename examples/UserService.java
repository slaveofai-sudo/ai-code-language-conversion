// 示例 Java 代码 - 用于测试转换功能
package com.example.demo;

import java.util.List;
import java.util.ArrayList;
import java.util.Optional;

/**
 * 用户服务类
 * 提供用户管理相关功能
 */
public class UserService {

    private List<User> users;

    public UserService() {
        this.users = new ArrayList<>();
    }

    /**
     * 添加用户
     * 
     * @param user 用户对象
     * @return 是否添加成功
     */
    public boolean addUser(User user) {
        if (user == null || user.getName() == null) {
            return false;
        }
        return users.add(user);
    }

    /**
     * 根据ID查找用户
     * 
     * @param id 用户ID
     * @return 用户对象（Optional）
     */
    public Optional<User> findUserById(int id) {
        return users.stream()
                .filter(u -> u.getId() == id)
                .findFirst();
    }

    /**
     * 获取所有用户
     * 
     * @return 用户列表
     */
    public List<User> getAllUsers() {
        return new ArrayList<>(users);
    }

    /**
     * 删除用户
     * 
     * @param id 用户ID
     * @return 是否删除成功
     */
    public boolean deleteUser(int id) {
        return users.removeIf(u -> u.getId() == id);
    }
}

/**
 * 用户实体类
 */
class User {
    private int id;
    private String name;
    private String email;

    public User(int id, String name, String email) {
        this.id = id;
        this.name = name;
        this.email = email;
    }

    public int getId() {
        return id;
    }

    public String getName() {
        return name;
    }

    public String getEmail() {
        return email;
    }

    @Override
    public String toString() {
        return String.format("User{id=%d, name='%s', email='%s'}", id, name, email);
    }
}
